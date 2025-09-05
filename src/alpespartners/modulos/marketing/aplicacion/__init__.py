from pydispatch import dispatcher
from .handlers import HandlerInteraccionDominio
from alpespartners.modulos.marketing.dominio.eventos import InteraccionRegistrada

dispatcher.connect(
    HandlerInteraccionDominio.handle_interaccion_registrada,
    signal='InteraccionRegistradaDominio',
)
