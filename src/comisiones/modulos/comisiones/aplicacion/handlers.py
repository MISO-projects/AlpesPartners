
from alpespartners.seedwork.aplicacion.handlers import Handler
from alpespartners.modulos.comisiones.dominio.eventos import (
    ComisionReservada,
    ComisionConfirmada,
    ComisionRevertida,
    ComisionCancelada,
    LoteComisionesConfirmadas,
    InteraccionAtribuidaRecibida
)
from alpespartners.modulos.comisiones.aplicacion.comandos.reservar_comision import (
    ReservarComision,
    ReservarComisionHandler
)
from alpespartners.modulos.comisiones.aplicacion.comandos.confirmar_comision import (
    ConfirmarComision,
    ConfirmarComisionHandler,
    ConfirmarComisionesEnLote,
    ConfirmarComisionesEnLoteHandler
)
from alpespartners.modulos.comisiones.aplicacion.comandos.revertir_comision import (
    RevertirComision,
    RevertirComisionHandler
)

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
            handler = ReservarComisionHandler()
            resultado = handler.handle(comando)

            print(f"Procesada InteraccionAtribuida {evento.id_interaccion} -> Comisión: {resultado.id if resultado else 'No generada'}")

        except Exception as e:
            print(f"Error procesando InteraccionAtribuidaRecibida {evento.id_interaccion}: {e}")
            raise e

class HandlerComisionReservada(Handler):

    def handle(self, evento: ComisionReservada):

        print(f"Comisión reservada: {evento.id_comision} para interacción {evento.id_interaccion}")

class HandlerComisionConfirmada(Handler):

    def handle(self, evento: ComisionConfirmada):

        print(f"Comisión confirmada: {evento.id_comision} - Monto: {evento.monto_confirmado.valor} {evento.monto_confirmado.moneda}")

class HandlerComisionRevertida(Handler):

    def handle(self, evento: ComisionRevertida):

        print(f"Comisión revertida: {evento.id_comision} - Motivo: {evento.motivo}")

class HandlerComisionCancelada(Handler):

    def handle(self, evento: ComisionCancelada):

        print(f"Comisión cancelada: {evento.id_comision} - Motivo: {evento.motivo}")

class HandlerLoteComisionesConfirmadas(Handler):

    def handle(self, evento: LoteComisionesConfirmadas):

        print(f"Lote de comisiones confirmadas: {evento.id_lote} - {evento.cantidad_comisiones} comisiones - Total: {evento.monto_total.valor} {evento.monto_total.moneda}")
def registrar_handlers():

    from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
    UnidadTrabajoPuerto.registrar_evento_handler(InteraccionAtribuidaRecibida, HandlerInteraccionAtribuidaRecibida())
    UnidadTrabajoPuerto.registrar_evento_handler(ComisionReservada, HandlerComisionReservada())
    UnidadTrabajoPuerto.registrar_evento_handler(ComisionConfirmada, HandlerComisionConfirmada())
    UnidadTrabajoPuerto.registrar_evento_handler(ComisionRevertida, HandlerComisionRevertida())
    UnidadTrabajoPuerto.registrar_evento_handler(ComisionCancelada, HandlerComisionCancelada())
    UnidadTrabajoPuerto.registrar_evento_handler(LoteComisionesConfirmadas, HandlerLoteComisionesConfirmadas())
