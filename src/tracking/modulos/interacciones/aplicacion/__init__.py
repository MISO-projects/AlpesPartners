from pydispatch import dispatcher
from .handlers import HandlerCampaniaDominio, HandlerInteraccionDominio

dispatcher.connect(
    HandlerCampaniaDominio.handle_campania_activada,
    signal=f'CampaniaActivadaDominio',
)
dispatcher.connect(
    HandlerInteraccionDominio.handle_interaccion_registrada,
    signal=f'InteraccionRegistradaDominio',
)
