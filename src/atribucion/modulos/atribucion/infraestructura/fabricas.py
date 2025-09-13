from dataclasses import dataclass
from atribucion.seedwork.dominio.fabricas import Fabrica
from atribucion.seedwork.dominio.repositorios import Repositorio
from atribucion.modulos.atribucion.dominio.repositorios import RepositorioJourney

from .repositorios import RepositorioJourneyMongoDB
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        
        if obj == RepositorioJourney.__class__:
            return RepositorioJourneyMongoDB()
        else:
            raise ExcepcionFabrica(f"No se puede crear un objeto de tipo {obj}")