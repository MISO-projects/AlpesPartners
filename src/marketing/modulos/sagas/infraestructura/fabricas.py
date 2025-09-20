from dataclasses import dataclass
from marketing.seedwork.dominio.fabricas import Fabrica
from marketing.modulos.sagas.dominio.repositorios import RepositorioSagaLog
from marketing.seedwork.dominio.excepciones import ExcepcionFabrica
from marketing.modulos.sagas.infraestructura.repositorios import RepositorioSagaLogPostgres


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> RepositorioSagaLog:
        if obj == RepositorioSagaLog.__class__:
            return RepositorioSagaLogPostgres()
        else:
            raise ExcepcionFabrica(f"No se puede crear un objeto de tipo {obj}")
