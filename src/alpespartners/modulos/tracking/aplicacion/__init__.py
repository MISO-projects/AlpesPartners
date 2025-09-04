from pydispatch import dispatcher
from .handlers import HandlerInteraccionIntegracion
from alpespartners.modulos.tracking.dominio.eventos import InteraccionRegistrada

dispatcher.connect(
    HandlerInteraccionIntegracion.handle_interaccion_registrada,
    signal=f'{InteraccionRegistrada.__name__}Integracion',
)
