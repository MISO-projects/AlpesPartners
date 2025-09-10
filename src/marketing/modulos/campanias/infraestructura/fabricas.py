from marketing.seedwork.dominio.fabricas import Fabrica
from marketing.modulos.campanias.dominio.repositorios import RepositorioCampania
from marketing.modulos.campanias.infraestructura.repositorios import (
    RepositorioCampaniaMongoDB,
)
from marketing.seedwork.dominio.excepciones import ExcepcionFabrica
from marketing.seedwork.dominio.repositorios import Repositorio


class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type) -> Repositorio:
        if obj == RepositorioCampania.__class__:
            return RepositorioCampaniaMongoDB()
        else:
            raise ExcepcionFabrica(
                f"No existe una fábrica concreta para el objeto de tipo {obj}"
            )
