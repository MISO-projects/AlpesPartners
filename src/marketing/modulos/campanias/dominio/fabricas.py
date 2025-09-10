from dataclasses import dataclass
from marketing.seedwork.dominio.fabricas import Fabrica
from marketing.seedwork.dominio.repositorios import Mapeador
from marketing.modulos.campanias.dominio.entidades import Campania
from marketing.seedwork.dominio.entidades import Entidad
from marketing.modulos.campanias.dominio.excepciones import (
    TipoCampaniaNoValidaExcepcion,
)


@dataclass
class _FabricaCampania(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            campania: Campania = mapeador.dto_a_entidad(obj)
            return campania


@dataclass
class FabricaCampania(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Campania.__class__:
            fabrica_campania = _FabricaCampania()
            return fabrica_campania.crear_objeto(obj, mapeador)
        else:
            raise TipoCampaniaNoValidaExcepcion(
                f"No se puede crear un objeto de tipo {mapeador.obtener_tipo()}"
            )
