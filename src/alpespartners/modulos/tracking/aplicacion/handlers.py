from alpespartners.seedwork.aplicacion.handlers import Handler


class HandlerCampaniaDominio(Handler):
    @staticmethod
    def handle_campania_activada(evento):
        print(f"Tracking: Evento CampaniaActivada recibido: {evento.nombre}")


class HandlerInteraccionDominio(Handler):
    @staticmethod
    def handle_interaccion_registrada(evento):
        print(f"Tracking: Evento InteraccionRegistrada recibido: {evento.tipo}")
