from pydispatch import dispatcher
from .handlers import HandlerInteraccionIntegracion
from atribucion.modulos.atribucion.dominio.eventos import InteraccionAtribuidaRecibida

dispatcher.connect(
    HandlerInteraccionIntegracion.handle_interaccion_atribuida_recibida,
    signal=f'{InteraccionAtribuidaRecibida.__name__}Integracion',
)