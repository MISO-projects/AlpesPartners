from tracking.seedwork.aplicacion.handlers import Handler
from tracking.modulos.interacciones.infraestructura.despachadores import DespachadorTracking


class HandlerCampaniaDominio(Handler):
    @staticmethod
    def handle_campania_activada(evento):
        print(f"Tracking: Evento CampaniaActivada recibido: {evento.nombre}")


class HandlerInteraccionDominio(Handler):
    @staticmethod
    def handle_interaccion_registrada(evento):
        print(f"Tracking: Evento InteraccionRegistrada recibido: {evento.tipo}")


class HandlerInteraccionIntegracion(Handler):
    @staticmethod
    def handle_interaccion_registrada(evento):
        despachador = DespachadorTracking()
        despachador.publicar_evento(evento, "interaccion-registrada")
