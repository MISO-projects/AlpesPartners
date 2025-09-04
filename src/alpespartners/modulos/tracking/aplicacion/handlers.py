from alpespartners.seedwork.aplicacion.handlers import Handler
from alpespartners.modulos.tracking.infraestructura.despachadores import Despachador


class HandlerInteraccionIntegracion(Handler):

    @staticmethod
    def handle_interaccion_registrada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, "interaccion-registrada")
