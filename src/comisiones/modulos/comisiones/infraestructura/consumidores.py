# pyright: reportUnreachable=false
import pulsar
import _pulsar
from pulsar.schema import AvroSchema, Record
import json
import traceback
import uuid
from decimal import Decimal

from comisiones.modulos.comisiones.infraestructura.schema.v1.eventos import EventoConversionAtribuida, EventoRevertirComision
from comisiones.seedwork.infraestructura import utils
from comisiones.modulos.comisiones.aplicacion.comandos.reservar_comision import ReservarComision
from comisiones.modulos.comisiones.aplicacion.comandos.revertir_comision_por_journey import RevertirComisionPorJourney

from comisiones.seedwork.aplicacion.comandos import ejecutar_commando

def avro_to_dict(record: Record) -> dict:
    if not isinstance(record, Record):
        return record
    
    result = {}
    for key, value in record.__dict__.items():
        if key.startswith('_'):
            continue
        if isinstance(value, Record):
            result[key] = avro_to_dict(value)
        elif isinstance(value, list):
            result[key] = [avro_to_dict(item) for item in value]
        else:
            result[key] = value
    return result

class ConsumidorEventosAtribucion:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_eventos_atribucion(self, app=None):
        if not app:
            return
            
        self.app = app
        try:
            print("COMISIONES: Conectando a Pulsar para consumir eventos de atribución...")
            self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            self.consumidor = self.cliente.subscribe(
                'eventos-atribucion',  # Tópico que publica el servicio de atribución
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='comisiones-sub-atribucion',
                schema=AvroSchema(EventoConversionAtribuida)
            )
            print("COMISIONES: Suscripción a eventos-atribucion exitosa")

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_conversion_atribuida(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f"COMISIONES: Error procesando conversión atribuida: {e}")
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)
        except Exception as e:
            print(f"COMISIONES: Error configurando consumidor de atribución: {e}")
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_conversion_atribuida(self, mensaje):
        """Procesar conversión atribuida y crear comisión"""
        try:
            evento_dict = avro_to_dict(mensaje.value().data)
            print(f"COMISIONES: Conversión atribuida recibida: {evento_dict}")
            
            id_interaccion_atribuida = evento_dict['id_interaccion_atribuida']
            id_campania = evento_dict['id_campania']
            id_afiliado = evento_dict['id_afiliado']
            tipo_conversion = evento_dict['tipo_conversion']
            monto_atribuido = evento_dict['monto_atribuido']
            score_fraude = evento_dict['score_fraude']
            
            print(f"COMISIONES: Procesando conversión {tipo_conversion} - Monto: {monto_atribuido['valor']} {monto_atribuido['moneda']}")
            print(f"COMISIONES: Datos recibidos - id_campania: '{id_campania}' (tipo: {type(id_campania)})")
            print(f"COMISIONES: Datos recibidos - id_interaccion_atribuida: '{id_interaccion_atribuida}' (tipo: {type(id_interaccion_atribuida)})")
            
            if tipo_conversion != 'PURCHASE':
                print(f"COMISIONES: Ignorando conversión de tipo {tipo_conversion}")
                return
            
            try:
                id_campania_clean = str(id_campania).strip()
                if not id_campania_clean or id_campania_clean == 'None':
                    print(f"COMISIONES: id_campania inválido o vacío: '{id_campania}'")
                    return
                
                id_interaccion_clean = str(id_interaccion_atribuida).strip()
                if not id_interaccion_clean or id_interaccion_clean == 'None':
                    print(f"COMISIONES: id_interaccion_atribuida inválido o vacío: '{id_interaccion_atribuida}'")
                    return
                
                print(f"COMISIONES: UUIDs limpiados - id_campania: '{id_campania_clean}', id_interaccion: '{id_interaccion_clean}'")
                
            except Exception as e:
                print(f"COMISIONES: Error validando UUIDs: {e}")
                return

            comando = ReservarComision(
                id_interaccion=uuid.UUID(id_interaccion_clean),
                id_campania=uuid.UUID(id_campania_clean),
                id_journey=uuid.UUID(id_interaccion_atribuida),
                tipo_interaccion=tipo_conversion,
                valor_interaccion=Decimal(str(monto_atribuido['valor'])),
                moneda_interaccion=monto_atribuido['moneda'],
                fraud_ok=score_fraude < 50,  # Considerar OK si score de fraude < 50
                score_fraude=score_fraude,
                parametros_adicionales={
                    'id_afiliado': id_afiliado,
                    'origen': 'atribucion',
                    'id_interaccion_original': evento_dict.get('id_interaccion_original', '')
                }
            )
            ejecutar_commando(comando)

                
        except Exception as e:
            print(f"COMISIONES: Error procesando conversión atribuida: {e}")
            traceback.print_exc()
            raise e

class ConsumidorEventosComision:

    def consumir_comision_reservada(self, evento: dict):
        print(f"COMISIONES: Procesando ComisionReservada: {evento.get('id_comision')}")

    def consumir_comision_confirmada(self, evento: dict):
        print(f"COMISIONES: Procesando ComisionConfirmada: {evento.get('id_comision')}")

    def consumir_lote_confirmado(self, evento: dict):
        print(f"COMISIONES: Procesando lote confirmado: {evento.get('id_lote')} - {evento.get('cantidad_comisiones')} comisiones")

class ConsumidorEventosReversion:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_eventos_reversion(self, app=None):
        if not app:
            return
            
        self.app = app
        try:
            print("COMISIONES: Conectando a Pulsar para consumir eventos de reversión...")
            self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
            self.consumidor = self.cliente.subscribe(
                'eventos-reversion-comision',  
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='comisiones-sub-reversion',
                schema=AvroSchema(EventoRevertirComision)
            )
            print("COMISIONES: Suscripción a eventos-reversion-comision exitosa")

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_reversion_comision(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f"COMISIONES: Error procesando reversión de comisión: {e}")
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)
        except Exception as e:
            print(f"COMISIONES: Error configurando consumidor de reversión: {e}")
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_reversion_comision(self, mensaje):
        try:
            evento_dict = avro_to_dict(mensaje.value().data)
            print(f"COMISIONES: Evento de reversión recibido: {evento_dict}")
            
            journey_id = evento_dict['journey_id']
            motivo = evento_dict['motivo']
            
            print(f"COMISIONES: Procesando reversión para journey_id: {journey_id} - Motivo: {motivo}")
            
            try:
                journey_id_clean = str(journey_id).strip()
                if not journey_id_clean or journey_id_clean == 'None':
                    print(f"COMISIONES: journey_id inválido o vacío: '{journey_id}'")
                    return
                
                print(f"COMISIONES: Journey ID limpio: '{journey_id_clean}'")
                
            except Exception as e:
                print(f"COMISIONES: Error validando journey_id: {e}")
                return

            comando = RevertirComisionPorJourney(
                journey_id=uuid.UUID(journey_id_clean),
                motivo=motivo
            )
            ejecutar_commando(comando)

        except Exception as e:
            print(f"COMISIONES: Error procesando reversión de comisión: {e}")
            traceback.print_exc()
            raise e