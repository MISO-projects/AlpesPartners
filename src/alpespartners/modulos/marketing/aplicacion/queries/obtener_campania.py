from alpespartners.seedwork.aplicacion.queries import Query, QueryResultado
from alpespartners.modulos.marketing.aplicacion.queries.base import (
    CampaniaQueryBaseHandler,
)
from alpespartners.modulos.marketing.dominio.repositorios import RepositorioCampania
from alpespartners.modulos.marketing.aplicacion.mapeadores import MapeadorCampania
from alpespartners.seedwork.aplicacion.queries import ejecutar_query as query
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
