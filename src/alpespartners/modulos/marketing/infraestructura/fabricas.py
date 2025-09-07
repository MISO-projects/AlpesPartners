from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.modulos.marketing.dominio.repositorios import RepositorioCampania
from alpespartners.modulos.marketing.infraestructura.repositorios import RepositorioCampaniaSQLite
from alpespartners.seedwork.dominio.excepciones import ExcepcionFabrica
from alpespartners.seedwork.dominio.repositorios import Repositorio


class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> Repositorio:
        if obj == RepositorioCampania.__class__:
            return RepositorioCampaniaSQLite()
        else:
            raise ExcepcionFabrica(f"No existe una fábrica concreta para el objeto de tipo {obj}")
