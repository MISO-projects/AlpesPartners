from alpespartners.seedwork.aplicacion.queries import Query, QueryResultado
from alpespartners.modulos.marketing.aplicacion.queries.base import (
    CampaniaQueryBaseHandler,
)
from alpespartners.modulos.marketing.dominio.repositorios import RepositorioCampania
from alpespartners.modulos.marketing.aplicacion.mapeadores import MapeadorCampania
from alpespartners.seedwork.aplicacion.queries import ejecutar_query as query
from dataclasses import dataclass


@dataclass
class ListarCampanias(Query):
    estado: str = None


class ListarCampaniasHandler(CampaniaQueryBaseHandler):
    def handle(self, query: ListarCampanias) -> QueryResultado:
        repositorio: RepositorioCampania = self.fabrica_repositorio.crear_objeto(
            RepositorioCampania.__class__
        )
        if query.estado == 'ACTIVA':
            campanias_dto = repositorio.obtener_activas()
        else:
            campanias_dto = repositorio.obtener_todos()
        campanias = [
            self.fabrica_campania.crear_objeto(campania_dto, MapeadorCampania())
            for campania_dto in campanias_dto
        ]
        return QueryResultado(campanias)


@query.register(ListarCampanias)
def ejecutar_query_obtener_campanias(query: ListarCampanias) -> QueryResultado:
    handler = ListarCampaniasHandler()
    return handler.handle(query)
