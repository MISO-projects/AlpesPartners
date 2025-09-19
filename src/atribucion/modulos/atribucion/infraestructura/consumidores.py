import pulsar
import _pulsar
from pulsar.schema import AvroSchema, Record
import json
import traceback

from atribucion.modulos.atribucion.infraestructura.schema.v1.eventos import EventoInteraccionRegistradaConsumo
from atribucion.seedwork.infraestructura import utils

from atribucion.modulos.atribucion.aplicacion.mapeadores import MapeadorAtribucionDTOJson
from atribucion.modulos.atribucion.aplicacion.comandos.registrar_atribucion import RegistrarAtribucion
from atribucion.seedwork.aplicacion.comandos import ejecutar_commando

def avro_to_dict(record: Record) -> dict:
    """Convierte un objeto Avro Record a un diccionario de Python recursivamente."""
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

class ConsumidorInteracciones:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_eventos_interaccion(self, app=None):
        if not app:
            return
            
        self.app = app
        try:
            self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
            self.consumidor = self.cliente.subscribe(
                'interaccion-registrada', 
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='atribucion-sub-interacciones',
                schema=AvroSchema(EventoInteraccionRegistradaConsumo)
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_mensaje_con_comando(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f"Error procesando InteraccionRegistrada: {e}")
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)
        except Exception as e:
            print(f"Error configurando consumidor de atribución: {e}")
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_mensaje_con_comando(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f"CONSUMIDOR: Evento recibido y convertido a dict: {evento_dict}")
        
        map_atribucion = MapeadorAtribucionDTOJson()
        atribucion_dto = map_atribucion.externo_a_dto(evento_dict)
        print(f"CONSUMIDOR: DTO creado a partir del dict: {atribucion_dto}")

        comando = RegistrarAtribucion(
            atribucion_dto=atribucion_dto,
            datos_evento_dict=evento_dict
        )
        print(f"CONSUMIDOR: Comando '{type(comando).__name__}' creado. Despachando...")
        ejecutar_commando(comando)



    def suscribirse_a_comandos_reversion(self, app=None):
        cliente = None
        try:
            from atribucion.modulos.atribucion.infraestructura.schema.v1.comandos import ComandoRevertirAtribucion
            
            cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
            
            consumidor = cliente.subscribe(
                'revertir-atribucion',
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='atribucion-sub-comandos-reversion',
                schema=AvroSchema(ComandoRevertirAtribucion)
            )
            print("Consumidor Atribucion: Esperando comandos RevertirAtribucion...")

            while True:
                mensaje = consumidor.receive()
                try:
                    self._procesar_mensaje_comando_reversion(mensaje)
                    consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f"Error procesando COMANDO de reversión: {e}")
                    traceback.print_exc()
                    consumidor.acknowledge(mensaje)

        except Exception as e:
            print(f"Error configurando consumidor de COMANDOS de reversión: {e}")
        finally:
            if cliente:
                cliente.close()

    def _procesar_mensaje_comando_reversion(self, mensaje):
        from atribucion.modulos.atribucion.aplicacion.comandos.revertir_atribucion import RevertirAtribucion
        
        payload = mensaje.value().data
        print(f"CONSUMIDOR: Comando 'RevertirAtribucion' recibido con payload: {payload}")
        
        comando = RevertirAtribucion(journey_id=payload.journey_id)
        ejecutar_commando(comando)
        
