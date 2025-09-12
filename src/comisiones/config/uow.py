from seedwork.infraestructura.uow import UnidadTrabajoPuerto
from seedwork.aplicacion.handlers import Handler
from typing import Dict, Type, Any
import logging

logger = logging.getLogger(__name__)


class ComisionesUnitOfWork(UnidadTrabajoPuerto):
    """
    Unidad de Trabajo específica para el módulo de comisiones
    Gestiona los handlers de eventos y coordina las operaciones transaccionales
    """
    
    def __init__(self):
        super().__init__()
        self._handlers: Dict[Type, Handler] = {}
        self._initialized = False
    
    def registrar_handler(self, evento_tipo: Type, handler: Handler):
        """Registrar un handler para un tipo de evento específico"""
        try:
            self._handlers[evento_tipo] = handler
            logger.info(f"Handler registrado para evento: {evento_tipo.__name__}")
        except Exception as e:
            logger.error(f"Error registrando handler para {evento_tipo.__name__}: {e}")
    
    def obtener_handler(self, evento_tipo: Type) -> Handler:
        """Obtener el handler para un tipo de evento"""
        return self._handlers.get(evento_tipo)
    
    def procesar_evento(self, evento):
        """Procesar un evento usando su handler correspondiente"""
        try:
            evento_tipo = type(evento)
            handler = self.obtener_handler(evento_tipo)
            
            if handler:
                logger.debug(f"Procesando evento {evento_tipo.__name__} con handler {handler.__class__.__name__}")
                handler.handle(evento)
            else:
                logger.warning(f"No se encontró handler para evento: {evento_tipo.__name__}")
                
        except Exception as e:
            logger.error(f"Error procesando evento {type(evento).__name__}: {e}")
            raise e
    
    def inicializar_handlers(self):
        """Inicializar todos los handlers del módulo de comisiones"""
        if self._initialized:
            logger.info("Handlers ya inicializados")
            return
        
        try:
            # Importar y registrar handlers de aplicación
            from modulos.comisiones.aplicacion.handlers import (
                HandlerInteraccionAtribuidaRecibida,
                HandlerComisionReservada,
                HandlerComisionConfirmada,
                HandlerComisionRevertida,
                HandlerComisionCancelada,
                HandlerLoteComisionesConfirmadas
            )
            
            # Importar tipos de eventos
            from modulos.comisiones.dominio.eventos import (
                InteraccionAtribuidaRecibida,
                ConversionAtribuida,  # Nuevo evento
                ComisionReservada,
                ComisionConfirmada,
                ComisionRevertida,
                ComisionCancelada,
                LoteComisionesConfirmadas
            )
            
            # Registrar handlers de aplicación
            self.registrar_handler(InteraccionAtribuidaRecibida, HandlerInteraccionAtribuidaRecibida())
            self.registrar_handler(ComisionReservada, HandlerComisionReservada())
            self.registrar_handler(ComisionConfirmada, HandlerComisionConfirmada())
            self.registrar_handler(ComisionRevertida, HandlerComisionRevertida())
            self.registrar_handler(ComisionCancelada, HandlerComisionCancelada())
            self.registrar_handler(LoteComisionesConfirmadas, HandlerLoteComisionesConfirmadas())
            
            # Registrar handler para el nuevo evento ConversionAtribuida
            self.registrar_handler(ConversionAtribuida, HandlerConversionAtribuida())
            
            # Registrar despachadores de infraestructura
            from modulos.comisiones.infraestructura.despachadores import registrar_despachadores
            registrar_despachadores()
            
            self._initialized = True
            logger.info("Todos los handlers del módulo de comisiones inicializados correctamente")
            
        except Exception as e:
            logger.error(f"Error inicializando handlers: {e}")
            raise e
    
    def limpiar_handlers(self):
        """Limpiar todos los handlers registrados"""
        self._handlers.clear()
        self._initialized = False
        logger.info("Handlers limpiados")


# Instancia global del UoW para el módulo de comisiones
_uow_instance = None


def get_unit_of_work() -> ComisionesUnitOfWork:
    """Obtener la instancia global del UoW"""
    global _uow_instance
    
    if _uow_instance is None:
        _uow_instance = ComisionesUnitOfWork()
        _uow_instance.inicializar_handlers()
    
    return _uow_instance


def inicializar_uow():
    """Función helper para inicializar el UoW desde otros módulos"""
    return get_unit_of_work()