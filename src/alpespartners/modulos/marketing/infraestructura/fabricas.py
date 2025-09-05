from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.modulos.marketing.dominio.repositorios import RepositorioCampania
from alpespartners.modulos.marketing.infraestructura.repositorios import RepositorioCampaniaSQLite


class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> object:
        if obj == RepositorioCampania:
            return RepositorioCampaniaSQLite()
        else:
            raise Exception(f"No existe una fábrica concreta para el objeto de tipo {obj}")
