from dataclasses import dataclass
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.marketing.dominio.entidades import Campania
from alpespartners.seedwork.dominio.entidades import Entidad
from alpespartners.modulos.marketing.dominio.excepciones import (
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
