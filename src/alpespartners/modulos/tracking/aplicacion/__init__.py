from pydispatch import dispatcher
from .handlers import HandlerInteraccionIntegracion
from alpespartners.modulos.tracking.dominio.eventos import InteraccionRegistrada

# TODO: Por ahora no usamos eventos de integracion
# dispatcher.connect(
#     HandlerInteraccionIntegracion.handle_interaccion_registrada,
#     signal=f'{InteraccionRegistrada.__name__}Integracion',
# )
