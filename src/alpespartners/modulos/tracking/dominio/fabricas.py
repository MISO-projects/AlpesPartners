from dataclasses import dataclass
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.tracking.dominio.entidades import Interaccion
from alpespartners.seedwork.dominio.entidades import Entidad
from alpespartners.modulos.tracking.dominio.excepciones import (
    TipoInteraccionNoValidoExcepcion,
)


@dataclass
class _FabricaInteraccion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            interaccion: Interaccion = mapeador.dto_a_entidad(obj)
            return interaccion


@dataclass
class FabricaInteraccion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Interaccion.__class__:
            fabrica_interaccion = _FabricaInteraccion()
            return fabrica_interaccion.crear_objeto(obj, mapeador)
        else:
            raise TipoInteraccionNoValidoExcepcion(
                f"No se puede crear un objeto de tipo {mapeador.obtener_tipo()}"
            )
