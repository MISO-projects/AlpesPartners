from .entidades import Journey
from .excepciones import TipoObjetoNoExisteEnDominioAtribucionExcepcion
from atribucion.seedwork.dominio.repositorios import Mapeador
from atribucion.seedwork.dominio.fabricas import Fabrica
from atribucion.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaAtribucion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            journey: Journey = mapeador.dto_a_entidad(obj)
            return journey

@dataclass
class FabricaAtribucion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Journey.__class__:
            fabrica_atribucion = _FabricaAtribucion()
            return fabrica_atribucion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAtribucionExcepcion()