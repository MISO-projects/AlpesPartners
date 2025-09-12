from dataclasses import dataclass
from tracking.seedwork.dominio.fabricas import Fabrica
from tracking.seedwork.dominio.repositorios import Repositorio
from tracking.modulos.interacciones.infraestructura.repositorios import (
    RepositorioInteraccionMongoDB,
)
from tracking.modulos.interacciones.infraestructura.excepciones import (
    NoExisteImplementacionParaTipoFabricaExcepcion,
)
from tracking.modulos.interacciones.dominio.repositorios import RepositorioInteraccion


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioInteraccion.__class__:
            return RepositorioInteraccionMongoDB()
        else:
            raise NoExisteImplementacionParaTipoFabricaExcepcion(
                f"No se puede crear un objeto de tipo {obj}"
            )
