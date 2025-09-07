from dataclasses import dataclass
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Repositorio
from alpespartners.modulos.tracking.infraestructura.repositorios import (
    RepositorioInteraccionMongoDB,
)
from alpespartners.modulos.tracking.infraestructura.excepciones import (
    NoExisteImplementacionParaTipoFabricaExcepcion,
)
from alpespartners.modulos.tracking.dominio.repositorios import RepositorioInteraccion


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioInteraccion.__class__:
            return RepositorioInteraccionMongoDB()
        else:
            raise NoExisteImplementacionParaTipoFabricaExcepcion(
                f"No se puede crear un objeto de tipo {obj}"
            )
