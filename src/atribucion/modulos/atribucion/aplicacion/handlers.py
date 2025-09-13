from atribucion.seedwork.aplicacion.handlers import Handler
from atribucion.modulos.atribucion.infraestructura.despachadores import DespachadorEventosAtribucion


class HandlerInteraccionIntegracion(Handler):
    
    @staticmethod
    def handle_interaccion_atribuida_recibida(evento):
        print(f"Atribucion: Publicando evento InteraccionAtribuidaRecibida de integracion: {evento.tipo_interaccion}")
        despachador = DespachadorEventosAtribucion()
        despachador.publicar_evento_conversion_atribuida(evento) 