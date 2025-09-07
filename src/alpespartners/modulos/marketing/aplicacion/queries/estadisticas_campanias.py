from alpespartners.seedwork.aplicacion.queries import Query, QueryResultado
from alpespartners.modulos.marketing.aplicacion.queries.base import (
    CampaniaQueryBaseHandler,
)
from alpespartners.modulos.marketing.dominio.repositorios import RepositorioCampania
from alpespartners.modulos.marketing.aplicacion.mapeadores import MapeadorCampania
from alpespartners.seedwork.aplicacion.queries import ejecutar_query as query
from dataclasses import dataclass


@dataclass
class EstadisticasCampaniasQuery(Query): ...


class EstadisticasCampaniasHandler(CampaniaQueryBaseHandler):
    def handle(self, query: EstadisticasCampaniasQuery) -> QueryResultado:
        repositorio: RepositorioCampania = self.fabrica_repositorio.crear_objeto(
            RepositorioCampania.__class__
        )

        todas_campanias = repositorio.obtener_todos()
        campanias_activas = repositorio.obtener_activas()

        total_impresiones = sum(c.metricas.impresiones for c in todas_campanias)
        total_clics = sum(c.metricas.clics for c in todas_campanias)
        total_conversiones = sum(c.metricas.conversiones for c in todas_campanias)
        costo_total = sum(c.metricas.costo_total for c in todas_campanias)

        ctr_promedio = (
            (total_clics / total_impresiones * 100) if total_impresiones > 0 else 0
        )
        cpc_promedio = (costo_total / total_clics) if total_clics > 0 else 0

        estadisticas = {
            "resumen": {
                "total_campanias": len(todas_campanias),
                "campanias_activas": len(campanias_activas),
                "total_impresiones": total_impresiones,
                "total_clics": total_clics,
                "total_conversiones": total_conversiones,
                "costo_total": costo_total,
                "ctr_promedio": round(ctr_promedio, 2),
                "cpc_promedio": round(cpc_promedio, 2),
            }
        }
        return QueryResultado(estadisticas)


@query.register(EstadisticasCampaniasQuery)
def ejecutar_query_estadisticas_campanias(
    query: EstadisticasCampaniasQuery,
) -> QueryResultado:
    handler = EstadisticasCampaniasHandler()
    return handler.handle(query)
