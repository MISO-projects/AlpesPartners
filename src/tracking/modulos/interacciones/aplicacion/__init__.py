from pydispatch import dispatcher
from .handlers import HandlerCampaniaDominio, HandlerInteraccionDominio, HandlerInteraccionIntegracion
from tracking.modulos.interacciones.dominio.eventos import InteraccionRegistrada

dispatcher.connect(
    HandlerCampaniaDominio.handle_campania_activada,
    signal=f'CampaniaActivadaDominio',
)
dispatcher.connect(
    HandlerInteraccionDominio.handle_interaccion_registrada,
    signal=f'InteraccionRegistradaDominio',
)
dispatcher.connect(
    HandlerInteraccionIntegracion.handle_interaccion_registrada,
    signal=f'{InteraccionRegistrada.__name__}Integracion',
)
