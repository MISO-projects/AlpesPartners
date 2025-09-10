
from alpespartners.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from alpespartners.modulos.comisiones.dominio.repositorios import RepositorioComision
from alpespartners.modulos.comisiones.dominio.excepciones import ComisionNoEncontradaExcepcion
from alpespartners.modulos.comisiones.aplicacion.mapeadores import MapeadorComision
from alpespartners.modulos.comisiones.aplicacion.dto import ComisionDTO
from alpespartners.modulos.comisiones.infraestructura.fabricas import FabricaRepositorio
from dataclasses import dataclass
import uuid

@dataclass
class ObtenerComision(Query):

    id_comision: uuid.UUID

class ObtenerComisionHandler(QueryHandler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        self._mapeador = MapeadorComision()

    def handle(self, query: ObtenerComision) -> QueryResultado:

        try:
            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )
            comision = repositorio.obtener_por_id(query.id_comision)
            if not comision:
                raise ComisionNoEncontradaExcepcion(f"Comisión {query.id_comision} no encontrada")
            comision_dto = self._mapeador.entidad_a_dto(comision)

            return QueryResultado(
                resultado=comision_dto,
                exitoso=True
            )

        except Exception as e:
            return QueryResultado(
                resultado=None,
                exitoso=False,
                error=str(e)
            )
