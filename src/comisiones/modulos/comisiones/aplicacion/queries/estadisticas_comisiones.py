
from comisiones.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado, ejecutar_query
from comisiones.modulos.comisiones.dominio.repositorios import (
    RepositorioComision,
    RepositorioConfiguracionComision,
    RepositorioPoliticaFraude
)
from comisiones.modulos.comisiones.dominio.servicios import ServicioComision
from comisiones.modulos.comisiones.aplicacion.dto import EstadisticasComisionDTO
from comisiones.modulos.comisiones.infraestructura.fabricas import FabricaRepositorio
from dataclasses import dataclass
import uuid

@dataclass
class ObtenerEstadisticasComisiones(Query):

    pass

@dataclass
class ObtenerEstadisticasComisionesPorCampania(Query):

    id_campania: uuid.UUID

class EstadisticasComisionesHandler(QueryHandler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

    def handle(self, query: Query) -> QueryResultado:

        try:
            if isinstance(query, ObtenerEstadisticasComisiones):
                return self._obtener_estadisticas_generales()
            elif isinstance(query, ObtenerEstadisticasComisionesPorCampania):
                return self._obtener_estadisticas_por_campania(query.id_campania)
            else:
                return QueryResultado(
                    resultado=None,
                    exitoso=False,
                    error="Tipo de query no soportado"
                )

        except Exception as e:
            return QueryResultado(
                resultado=None,
                exitoso=False,
                error=str(e)
            )

    def _obtener_estadisticas_generales(self) -> QueryResultado:

        repositorio = self._fabrica_repositorio.crear_objeto(
            RepositorioComision.__class__
        )

        todas_comisiones = repositorio.obtener_todos()
        
        estadisticas = self._calcular_estadisticas(todas_comisiones)

        return QueryResultado(
            resultado=estadisticas,
            exitoso=True
        )

    def _obtener_estadisticas_por_campania(self, id_campania: uuid.UUID) -> QueryResultado:
        repositorio_comision = self._fabrica_repositorio.crear_objeto(
            RepositorioComision.__class__
        )
        repositorio_configuracion = self._fabrica_repositorio.crear_objeto(
            RepositorioConfiguracionComision.__class__
        )
        repositorio_politica_fraude = self._fabrica_repositorio.crear_objeto(
            RepositorioPoliticaFraude.__class__
        )
        servicio_comision = ServicioComision(
            repositorio_comision=repositorio_comision,
            repositorio_configuracion=repositorio_configuracion,
            repositorio_politica_fraude=repositorio_politica_fraude
        )
        estadisticas_dict = servicio_comision.calcular_comisiones_totales_campania(id_campania)
        estadisticas_dto = EstadisticasComisionDTO(
            total_comisiones=estadisticas_dict["total_comisiones"],
            reservadas=estadisticas_dict["reservadas"],
            confirmadas=estadisticas_dict["confirmadas"],
            revertidas=estadisticas_dict["revertidas"],
            canceladas=estadisticas_dict["canceladas"],
            monto_total_reservado=estadisticas_dict["monto_total_reservado"],
            monto_total_confirmado=estadisticas_dict["monto_total_confirmado"],
            monto_total_revertido=estadisticas_dict["monto_total_revertido"]
        )

        return QueryResultado(
            resultado=estadisticas_dto,
            exitoso=True
        )

    def _calcular_estadisticas(self, comisiones) -> EstadisticasComisionDTO:

        from comisiones.modulos.comisiones.dominio.objetos_valor import EstadoComision
        from decimal import Decimal

        estadisticas = {
            "total_comisiones": len(comisiones),
            "reservadas": 0,
            "confirmadas": 0,
            "revertidas": 0,
            "canceladas": 0,
            "monto_total_reservado": Decimal('0'),
            "monto_total_confirmado": Decimal('0'),
            "monto_total_revertido": Decimal('0')
        }

        for comision in comisiones:
            if comision.estado == EstadoComision.RESERVADA:
                estadisticas["reservadas"] += 1
                estadisticas["monto_total_reservado"] += comision.monto.valor
            elif comision.estado == EstadoComision.CONFIRMADA:
                estadisticas["confirmadas"] += 1
                estadisticas["monto_total_confirmado"] += comision.monto.valor
            elif comision.estado == EstadoComision.REVERTIDA:
                estadisticas["revertidas"] += 1
                estadisticas["monto_total_revertido"] += comision.monto.valor
            elif comision.estado == EstadoComision.CANCELADA:
                estadisticas["canceladas"] += 1

        return EstadisticasComisionDTO(
            total_comisiones=estadisticas["total_comisiones"],
            reservadas=estadisticas["reservadas"],
            confirmadas=estadisticas["confirmadas"],
            revertidas=estadisticas["revertidas"],
            canceladas=estadisticas["canceladas"],
            monto_total_reservado=estadisticas["monto_total_reservado"],
            monto_total_confirmado=estadisticas["monto_total_confirmado"],
            monto_total_revertido=estadisticas["monto_total_revertido"]
        )


@ejecutar_query.register
def _(query: ObtenerEstadisticasComisiones):
    handler = EstadisticasComisionesHandler()
    return handler.handle(query)


@ejecutar_query.register
def _(query: ObtenerEstadisticasComisionesPorCampania):
    handler = EstadisticasComisionesHandler()
    return handler.handle(query)
