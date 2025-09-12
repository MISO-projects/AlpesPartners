from pydispatch import dispatcher
from .handlers import (
    HandlerInteraccionAtribuidaRecibida,
    HandlerComisionReservada,
    HandlerComisionConfirmada,
    HandlerComisionRevertida,
    HandlerComisionCancelada,
    HandlerLoteComisionesConfirmadas,
    HandlerConversionAtribuida,
    HandlerComisionCalculada
)
from comisiones.modulos.comisiones.dominio.eventos import (
    ComisionReservada,
    ComisionCalculada,
    ComisionConfirmada,
    ComisionRevertida,
    ComisionCancelada,
    LoteComisionesConfirmadas,
    InteraccionAtribuidaRecibida,
    ConversionAtribuida
)

dispatcher.connect(HandlerComisionReservada().handle, signal=f'{ComisionReservada.__name__}Integracion')
dispatcher.connect(HandlerComisionCalculada().handle, signal=f'{ComisionCalculada.__name__}Integracion')
dispatcher.connect(HandlerComisionConfirmada().handle, signal=f'{ComisionConfirmada.__name__}Integracion')
dispatcher.connect(HandlerComisionRevertida().handle, signal=f'{ComisionRevertida.__name__}Integracion')
dispatcher.connect(HandlerComisionCancelada().handle, signal=f'{ComisionCancelada.__name__}Integracion')
dispatcher.connect(HandlerLoteComisionesConfirmadas().handle, signal=f'{LoteComisionesConfirmadas.__name__}Integracion')
dispatcher.connect(HandlerInteraccionAtribuidaRecibida().handle, signal=f'{InteraccionAtribuidaRecibida.__name__}Integracion')
dispatcher.connect(HandlerConversionAtribuida().handle, signal=f'{ConversionAtribuida.__name__}Integracion')
