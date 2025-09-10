
from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpespartners.modulos.comisiones.dominio.eventos import (
    ComisionReservada,
    ComisionConfirmada,
    ComisionRevertida,
    ComisionCancelada,
    LoteComisionesConfirmadas,
    PoliticaFraudeAplicada
)
from alpespartners.modulos.comisiones.infraestructura.consumidores import ConsumidorEventosComision
from datetime import datetime
import json

class DespachadorEventosComision:

    def __init__(self):
        self._consumidor = ConsumidorEventosComision()

    def despachar_comision_reservada(self, evento: ComisionReservada):

        try:
            evento_dict = {
                'tipo': 'ComisionReservada',
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
                }
            }

            self._consumidor.consumir_comision_reservada(evento_dict)

            self._publicar_evento_externo('comision.reservada', evento_dict)

            print(f"Evento ComisionReservada despachado exitosamente: {evento.id_comision}")

        except Exception as e:
            print(f"Error despachando ComisionReservada: {e}")

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
            evento_dict = {
                'tipo': 'ComisionRevertida',
                'id_comision': str(evento.id_comision),
                'monto_revertido': {
                    'valor': str(evento.monto_revertido.valor),
                    'moneda': evento.monto_revertido.moneda
                },
                'motivo': evento.motivo,
                'fecha_reversion': evento.fecha_reversion.isoformat()
            }

            self._publicar_evento_externo('comision.revertida', evento_dict)

            print(f"Evento ComisionRevertida despachado exitosamente: {evento.id_comision}")

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

    despachador = DespachadorEventosComision()
    
    UnidadTrabajoPuerto.registrar_evento_handler(
        ComisionReservada, 
        despachador.despachar_comision_reservada
    )
    
    UnidadTrabajoPuerto.registrar_evento_handler(
        ComisionConfirmada,
        despachador.despachar_comision_confirmada
    )
    
    UnidadTrabajoPuerto.registrar_evento_handler(
        ComisionRevertida,
        despachador.despachar_comision_revertida
    )
    
    UnidadTrabajoPuerto.registrar_evento_handler(
        ComisionCancelada,
        despachador.despachar_comision_cancelada
    )
    
    UnidadTrabajoPuerto.registrar_evento_handler(
        LoteComisionesConfirmadas,
        despachador.despachar_lote_confirmado
    )
    
    UnidadTrabajoPuerto.registrar_evento_handler(
        PoliticaFraudeAplicada,
        despachador.despachar_politica_fraude_aplicada
    )
    
    print("Despachadores de eventos de comisiones registrados")
