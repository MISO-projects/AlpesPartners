
from alpespartners.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from alpespartners.modulos.comisiones.dominio.repositorios import RepositorioComision
from alpespartners.modulos.comisiones.dominio.objetos_valor import EstadoComision
from alpespartners.modulos.comisiones.aplicacion.mapeadores import MapeadorComision
from alpespartners.modulos.comisiones.aplicacion.dto import ComisionDTO
from alpespartners.modulos.comisiones.infraestructura.fabricas import FabricaRepositorio
from dataclasses import dataclass
from typing import List, Optional
import uuid

@dataclass
class ListarComisiones(Query):

    pass

@dataclass
class ListarComisionesPorEstado(Query):

    estado: str

@dataclass
class ListarComisionesPorCampania(Query):

    id_campania: uuid.UUID

@dataclass
class ListarComisionesReservadasParaLote(Query):

    limite: int = 100

class ListarComisionesHandler(QueryHandler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        self._mapeador = MapeadorComision()

    def handle(self, query: Query) -> QueryResultado:

        try:
            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )

            if isinstance(query, ListarComisiones):
                return self._listar_todas(repositorio)
            elif isinstance(query, ListarComisionesPorEstado):
                return self._listar_por_estado(repositorio, query)
            elif isinstance(query, ListarComisionesPorCampania):
                return self._listar_por_campania(repositorio, query)
            elif isinstance(query, ListarComisionesReservadasParaLote):
                return self._listar_para_lote(repositorio, query)
            else:
                return QueryResultado(
                    resultado=[],
                    exitoso=False,
                    error="Tipo de query no soportado"
                )

        except Exception as e:
            return QueryResultado(
                resultado=[],
                exitoso=False,
                error=str(e)
            )

    def _listar_todas(self, repositorio: RepositorioComision) -> QueryResultado:

        comisiones = repositorio.obtener_todos()
        comisiones_dto = [
            self._mapeador.entidad_a_dto(comision) 
            for comision in comisiones
        ]

        return QueryResultado(
            resultado=comisiones_dto,
            exitoso=True
        )

    def _listar_por_estado(self, repositorio: RepositorioComision, query: ListarComisionesPorEstado) -> QueryResultado:

        estado = EstadoComision(query.estado)
        comisiones = repositorio.obtener_por_estado(estado)
        
        comisiones_dto = [
            self._mapeador.entidad_a_dto(comision) 
            for comision in comisiones
        ]

        return QueryResultado(
            resultado=comisiones_dto,
            exitoso=True
        )

    def _listar_por_campania(self, repositorio: RepositorioComision, query: ListarComisionesPorCampania) -> QueryResultado:

        comisiones = repositorio.obtener_por_campania(query.id_campania)
        
        comisiones_dto = [
            self._mapeador.entidad_a_dto(comision) 
            for comision in comisiones
        ]

        return QueryResultado(
            resultado=comisiones_dto,
            exitoso=True
        )

    def _listar_para_lote(self, repositorio: RepositorioComision, query: ListarComisionesReservadasParaLote) -> QueryResultado:

        comisiones = repositorio.obtener_para_lote(query.limite)
        
        comisiones_dto = [
            self._mapeador.entidad_a_dto(comision) 
            for comision in comisiones
        ]

        return QueryResultado(
            resultado=comisiones_dto,
            exitoso=True
        )
