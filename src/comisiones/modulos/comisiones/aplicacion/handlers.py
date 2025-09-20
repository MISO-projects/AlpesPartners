
from comisiones.seedwork.aplicacion.handlers import Handler
from comisiones.modulos.comisiones.dominio.eventos import (
    ComisionReservada,
    ComisionCalculada,
    ComisionConfirmada,
    ComisionRevertida,
    ComisionCancelada,
    LoteComisionesConfirmadas,
    InteraccionAtribuidaRecibida,
    ConversionAtribuida
)
from comisiones.modulos.comisiones.aplicacion.comandos.reservar_comision import ReservarComision
from comisiones.modulos.comisiones.aplicacion.comandos.calcular_comision import CalcularComision
from comisiones.modulos.comisiones.aplicacion.comandos.confirmar_comision import (
    ConfirmarComision,
    ConfirmarComisionesEnLote
)
from comisiones.modulos.comisiones.aplicacion.comandos.revertir_comision import RevertirComision
from comisiones.seedwork.aplicacion.comandos import ejecutar_commando
from comisiones.modulos.comisiones.infraestructura.despachadores import DespachadorEventosComision

class HandlerInteraccionAtribuidaRecibida(Handler):

    def handle(self, evento: InteraccionAtribuidaRecibida):

        try:
            comando = ReservarComision(
                id_interaccion=evento.id_interaccion,
                id_campania=evento.id_campania,
                tipo_interaccion=evento.tipo_interaccion,
                valor_interaccion=evento.valor_interaccion.valor,
                moneda_interaccion=evento.valor_interaccion.moneda,
                fraud_ok=evento.fraud_ok,
                score_fraude=evento.score_fraude
            )
            resultado = ejecutar_commando(comando)

            print(f"Procesada InteraccionAtribuida {evento.id_interaccion} -> Comisión: {resultado.id if resultado else 'No generada'}")

        except Exception as e:
            print(f"Error procesando InteraccionAtribuidaRecibida {evento.id_interaccion}: {e}")
            raise e

class HandlerComisionReservada(Handler):

    @staticmethod
    def handle(evento: ComisionReservada):
        despachador = DespachadorEventosComision()
        despachador.despachar_comision_reservada(evento)
        print(f"Comisión reservada: {evento.id_comision} para journey {evento.id_journey}")

class HandlerComisionConfirmada(Handler):

    def handle(self, evento: ComisionConfirmada):

        print(f"Comisión confirmada: {evento.id_comision} - Monto: {evento.monto_confirmado.valor} {evento.monto_confirmado.moneda}")

class HandlerComisionRevertida(Handler):

    @staticmethod
    def handle(evento: ComisionRevertida):
        despachador = DespachadorEventosComision()
        despachador.despachar_comision_revertida(evento)
        print(f"Comisión revertida: {evento.id_comision} - Journey ID: {evento.journey_id} - Motivo: {evento.motivo}")

class HandlerComisionCancelada(Handler):

    def handle(self, evento: ComisionCancelada):

        print(f"Comisión cancelada: {evento.id_comision} - Motivo: {evento.motivo}")

class HandlerLoteComisionesConfirmadas(Handler):

    def handle(self, evento: LoteComisionesConfirmadas):

        print(f"Lote de comisiones confirmadas: {evento.id_lote} - {evento.cantidad_comisiones} comisiones - Total: {evento.monto_total.valor} {evento.monto_total.moneda}")

class HandlerConversionAtribuida(Handler):
    """Handler para procesar eventos de conversión atribuida del AttributionService"""

    def handle(self, evento: ConversionAtribuida):
        try:
            print(f"Procesando ConversionAtribuida: {evento.id_interaccion} -> Campaña: {evento.id_campania}")
            
            comando = CalcularComision(
                id_interaccion=evento.id_interaccion,
                id_campania=evento.id_campania,
                tipo_interaccion=evento.tipo_interaccion,
                valor_interaccion=evento.valor_interaccion.valor,
                moneda_interaccion=evento.valor_interaccion.moneda,
                fraud_ok=evento.fraud_ok,
                score_fraude=evento.score_fraude,
                parametros_adicionales=evento.atribucion_data
            )
            
            resultado = ejecutar_commando(comando)
            
            print(f"ConversionAtribuida {evento.id_interaccion} procesada -> Comisión: {resultado.id if resultado else 'No generada'}")
            
        except Exception as e:
            print(f"Error procesando ConversionAtribuida {evento.id_interaccion}: {e}")
            raise e

class HandlerComisionCalculada(Handler):

    def handle(self, evento: ComisionCalculada):
        try:
            print(f"Comisión calculada exitosamente: {evento.id_comision} para interacción {evento.id_interaccion}")
            print(f"  Monto: {evento.monto.valor} {evento.monto.moneda}")
            print(f"  Tipo de cálculo: {evento.tipo_calculo}")
            print(f"  Campaña: {evento.id_campania}")
        except Exception as e:
            print(f"Error procesando ComisionCalculada {evento.id_comision}: {e}")
            raise e


from pydispatch import dispatcher
