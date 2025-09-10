from pydispatch import dispatcher
from .handlers import HandlerCampaniaIntegracion
from marketing.modulos.campanias.dominio.eventos import CampaniaCreada, CampaniaActivada

dispatcher.connect(
    HandlerCampaniaIntegracion.handle_campania_creada,
    signal=f'{CampaniaCreada.__name__}Integracion',
)
dispatcher.connect(
    HandlerCampaniaIntegracion.handle_campania_activada,
    signal=f'{CampaniaActivada.__name__}Integracion',
)
