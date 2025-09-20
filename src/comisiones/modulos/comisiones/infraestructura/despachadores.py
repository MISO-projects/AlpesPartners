from comisiones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from comisiones.modulos.comisiones.dominio.eventos import (
    ComisionReservada,
    ComisionCalculada,
    ComisionConfirmada,
    ComisionRevertida,
    ComisionCancelada,
    LoteComisionesConfirmadas,
    PoliticaFraudeAplicada
)
from comisiones.modulos.comisiones.infraestructura.consumidores import ConsumidorEventosComision
from datetime import datetime
import json
import pulsar
from pulsar.schema import AvroSchema
from comisiones.modulos.comisiones.infraestructura.schema.v1.eventos import (
    EventoComisionReservada,
    EventoComisionCalculada,
    ComisionReservadaPayload,
    ComisionCalculadaPayload,
    ComisionRevertidaPayload,
    EventoComisionRevertidaIntegracion
)
from comisiones.seedwork.infraestructura import utils

class DespachadorEventosComision:

    def __init__(self):
        self._consumidor = ConsumidorEventosComision()
    
    def _publicar_mensaje_pulsar(self, mensaje, topico, schema_class):
        try:
            print(f"COMISIONES: Conectando al broker Pulsar para publicar en {topico}...")
            cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema_class))
            
            print(f"COMISIONES: Publicando mensaje en tópico: {topico}")
            publicador.send(mensaje)
            
            print(f"COMISIONES: Mensaje publicado exitosamente en {topico}")
            cliente.close()
        except Exception as e:
            print(f"COMISIONES: Error publicando mensaje en {topico}: {e}")

    def despachar_comision_reservada(self, evento: ComisionReservada):

        try:
            payload = ComisionReservadaPayload(
                id_correlacion=evento.id_correlacion,
                id_journey=str(evento.id_journey),
                id_comision=str(evento.id_comision),
                id_campania=str(evento.id_campania),
                monto={
                    'valor': float(evento.monto.valor),
                    'moneda': evento.monto.moneda
                },
                configuracion={
                    'tipo': evento.configuracion.tipo.value,
                    'porcentaje': float(evento.configuracion.porcentaje) if evento.configuracion.porcentaje else 0.0
                },
                timestamp=evento.timestamp.isoformat(),
                fraud_ok=True,
                score_fraude=0
            )
            
            evento_pulsar = EventoComisionReservada(
                correlation_id=str(evento.id_comision),
                message_id=f"comision-reservada-{evento.id_comision}",
                type="ComisionReservada",
                ingestion=int(datetime.now().timestamp() * 1000),
                datacontenttype="application/json",
                service_name="comisiones",
                data=payload
            )

            self._publicar_mensaje_pulsar(evento_pulsar, 'comision-reservada', EventoComisionReservada)

            print(f"COMISIONES: Evento ComisionReservada despachado exitosamente: {evento.id_comision}")

        except Exception as e:
            print(f"COMISIONES: Error despachando ComisionReservada: {e}")

    def despachar_comision_calculada(self, evento: ComisionCalculada):

        try:
            evento_dict = {
                'tipo': 'ComisionCalculada',
                'id_comision': str(evento.id_comision),
                'id_interaccion': str(evento.id_interaccion),
                'id_campania': str(evento.id_campania),
                'monto': {
                    'valor': str(evento.monto.valor),
                    'moneda': evento.monto.moneda
                },
                'configuracion': {
                    'tipo': evento.configuracion.tipo.value,
                    'porcentaje': str(evento.configuracion.porcentaje) if evento.configuracion.porcentaje else None
                },
                'timestamp': evento.timestamp.isoformat(),
                'politica_fraude': {
                    'tipo': evento.politica_fraude.tipo.value,
                    'threshold_score': evento.politica_fraude.threshold_score
                },
                'tipo_calculo': evento.tipo_calculo
            }

            self._publicar_evento_externo('comisionCalculada', evento_dict)

            print(f"Evento ComisionCalculada despachado exitosamente: {evento.id_comision}")
            print(f"  -> Publicado evento externo: comisionCalculada")

        except Exception as e:
            print(f"Error despachando ComisionCalculada: {e}")

    def despachar_comision_confirmada(self, evento: ComisionConfirmada):

        try:
            evento_dict = {
                'tipo': 'ComisionConfirmada',
                'id_comision': str(evento.id_comision),
                'monto_confirmado': {
                    'valor': str(evento.monto_confirmado.valor),
                    'moneda': evento.monto_confirmado.moneda
                },
                'lote_confirmacion': evento.lote_confirmacion,
                'fecha_confirmacion': evento.fecha_confirmacion.isoformat()
            }

            self._consumidor.consumir_comision_confirmada(evento_dict)

            self._publicar_evento_externo('comision.confirmada', evento_dict)

            print(f"Evento ComisionConfirmada despachado exitosamente: {evento.id_comision}")

        except Exception as e:
            print(f"Error despachando ComisionConfirmada: {e}")

    def despachar_comision_revertida(self, evento: ComisionRevertida):
        try:
            payload = ComisionRevertidaPayload(
                id_correlacion=evento.id_correlacion,
                id_comision=str(evento.id_comision),
                journey_id=str(evento.journey_id),
                monto_revertido={
                    'valor': float(evento.monto_revertido.valor),
                    'moneda': evento.monto_revertido.moneda
                },
                motivo=evento.motivo,
                fecha_reversion=evento.fecha_reversion.isoformat()
            )
            evento = EventoComisionRevertidaIntegracion(data=payload)
            self._publicar_mensaje_pulsar(
                evento, 'comision-revertida', EventoComisionRevertidaIntegracion
            )

            print(
                f"Evento ComisionRevertida despachado exitosamente: {evento.id_comision}"
            )

        except Exception as e:
            print(f"Error despachando ComisionRevertida: {e}")

    def despachar_comision_cancelada(self, evento: ComisionCancelada):

        try:
            evento_dict = {
                'tipo': 'ComisionCancelada',
                'id_comision': str(evento.id_comision),
                'motivo': evento.motivo,
                'fecha_cancelacion': evento.fecha_cancelacion.isoformat()
            }

            self._publicar_evento_externo('comision.cancelada', evento_dict)

            print(f"Evento ComisionCancelada despachado exitosamente: {evento.id_comision}")

        except Exception as e:
            print(f"Error despachando ComisionCancelada: {e}")

    def despachar_lote_confirmado(self, evento: LoteComisionesConfirmadas):

        try:
            evento_dict = {
                'tipo': 'LoteComisionesConfirmadas',
                'id_lote': evento.id_lote,
                'comisiones_confirmadas': [str(id_comision) for id_comision in evento.comisiones_confirmadas],
                'monto_total': {
                    'valor': str(evento.monto_total.valor),
                    'moneda': evento.monto_total.moneda
                },
                'fecha_confirmacion': evento.fecha_confirmacion.isoformat(),
                'cantidad_comisiones': evento.cantidad_comisiones
            }

            self._consumidor.consumir_lote_confirmado(evento_dict)

            self._publicar_evento_externo('lote.confirmado', evento_dict)

            print(f"Evento LoteComisionesConfirmadas despachado exitosamente: {evento.id_lote}")

        except Exception as e:
            print(f"Error despachando LoteComisionesConfirmadas: {e}")

    def despachar_politica_fraude_aplicada(self, evento: PoliticaFraudeAplicada):

        try:
            evento_dict = {
                'tipo': 'PoliticaFraudeAplicada',
                'id_comision': str(evento.id_comision),
                'id_interaccion': str(evento.id_interaccion),
                'score_fraude': evento.score_fraude,
                'politica_aplicada': {
                    'tipo': evento.politica_aplicada.tipo.value,
                    'threshold_score': evento.politica_aplicada.threshold_score
                },
                'resultado': evento.resultado
            }

            self._publicar_evento_externo('fraude.evaluado', evento_dict)

            print(f"Evento PoliticaFraudeAplicada despachado: {evento.id_comision} - {evento.resultado}")

        except Exception as e:
            print(f"Error despachando PoliticaFraudeAplicada: {e}")

    def _publicar_evento_externo(self, tipo_evento: str, datos_evento: dict):

        try:
            
            mensaje = {
                'timestamp': datetime.now().isoformat(),
                'servicio': 'comisiones',
                'tipo_evento': tipo_evento,
                'datos': datos_evento
            }

            print(f"Publicando evento externo: {tipo_evento}")
            print(f"   Datos: {json.dumps(mensaje, indent=2)}")

        except Exception as e:
            print(f"Error publicando evento externo {tipo_evento}: {e}")

    def _enviar_webhook(self, url: str, datos: dict):

        try:
            import requests
            
            response = requests.post(
                url,
                json=datos,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"Webhook enviado exitosamente a {url}")
            else:
                print(f"Error en webhook a {url}: {response.status_code}")

        except Exception as e:
            print(f"Error enviando webhook a {url}: {e}")

    def _registrar_auditoria(self, evento_dict: dict):

        try:
            
            registro_auditoria = {
                'timestamp': datetime.now().isoformat(),
                'modulo': 'comisiones',
                'evento': evento_dict,
                'usuario': 'sistema',
                'ip': '127.0.0.1'
            }

            print(f"Registro de auditoría: {evento_dict.get('tipo')}")

        except Exception as e:
            print(f"Error registrando auditoría: {e}")

def registrar_despachadores():
    from pydispatch import dispatcher
    
    despachador = DespachadorEventosComision()
    
    dispatcher.connect(
        despachador.despachar_comision_reservada,
        signal=f'{ComisionReservada.__name__}Dominio'
    )
    
    dispatcher.connect(
        despachador.despachar_comision_calculada,
        signal=f'{ComisionCalculada.__name__}Dominio'
    )
    
    dispatcher.connect(
        despachador.despachar_comision_confirmada,
        signal=f'{ComisionConfirmada.__name__}Dominio'
    )
    
    dispatcher.connect(
        despachador.despachar_comision_revertida,
        signal=f'{ComisionRevertida.__name__}Dominio'
    )
    
    dispatcher.connect(
        despachador.despachar_comision_cancelada,
        signal=f'{ComisionCancelada.__name__}Dominio'
    )
    
    dispatcher.connect(
        despachador.despachar_lote_confirmado,
        signal=f'{LoteComisionesConfirmadas.__name__}Dominio'
    )
    
    dispatcher.connect(
        despachador.despachar_politica_fraude_aplicada,
        signal=f'{PoliticaFraudeAplicada.__name__}Dominio'
    )
    
    print("Despachadores de eventos de comisiones registrados")
