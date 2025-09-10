from marketing.seedwork.aplicacion.queries import Query, QueryResultado
from marketing.modulos.campanias.aplicacion.queries.base import (
    CampaniaQueryBaseHandler,
)
from marketing.modulos.campanias.dominio.repositorios import RepositorioCampania
from marketing.modulos.campanias.aplicacion.mapeadores import MapeadorCampania
from marketing.seedwork.aplicacion.queries import ejecutar_query as query
from dataclasses import dataclass


@dataclass
class ObtenerCampania(Query):
    id: str


class ObtenerCampaniaHandler(CampaniaQueryBaseHandler):
    def handle(self, query: ObtenerCampania) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(
            RepositorioCampania.__class__
        )
        campania = self.fabrica_campania.crear_objeto(
            repositorio.obtener_por_id(query.id), MapeadorCampania()
        )
        return QueryResultado(campania)


@query.register(ObtenerCampania)
def ejecutar_query_obtener_campania(query: ObtenerCampania) -> QueryResultado:
    handler = ObtenerCampaniaHandler()
    return handler.handle(query)
