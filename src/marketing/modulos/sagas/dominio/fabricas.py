from dataclasses import dataclass
from marketing.seedwork.dominio.fabricas import Fabrica
from marketing.seedwork.dominio.repositorios import Mapeador
from marketing.modulos.sagas.dominio.entidades import SagaLog
from marketing.seedwork.dominio.entidades import Entidad
from marketing.modulos.sagas.dominio.excepciones import TipoSagaLogNoValidaExcepcion


@dataclass
class _FabricaSagaLog(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            saga_log: SagaLog = mapeador.dto_a_entidad(obj)
            return saga_log


@dataclass
class FabricaSagaLog(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == SagaLog.__class__:
            fabrica_saga_log = _FabricaSagaLog()
            return fabrica_saga_log.crear_objeto(obj, mapeador)
        else:
            raise TipoSagaLogNoValidaExcepcion(
                f"No se puede crear un objeto de tipo {mapeador.obtener_tipo()}"
            )
