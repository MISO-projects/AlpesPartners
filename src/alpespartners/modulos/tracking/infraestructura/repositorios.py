from uuid import UUID
from alpespartners.modulos.tracking.dominio.repositorios import RepositorioInteraccion
from alpespartners.modulos.tracking.dominio.fabricas import FabricaInteraccion
from alpespartners.modulos.tracking.dominio.entidades import Interaccion
from alpespartners.modulos.tracking.infraestructura.mapeadores import (
    MapeadorInteraccion,
)
from alpespartners.modulos.tracking.infraestructura.dto import InteraccionDbDto
from alpespartners.config.db import db
from alpespartners.seedwork.dominio.entidades import Entidad


# TODO: Change to a real database
class RepositorioInteraccionSQLite(RepositorioInteraccion):
    def __init__(self):
        self._fabrica_interaccion: FabricaInteraccion = FabricaInteraccion()

    @property
    def fabrica_interaccion(self) -> FabricaInteraccion:
        return self._fabrica_interaccion

    def obtener_por_id(self, id: UUID) -> Interaccion:
        interaccion_dto = db.session.query(InteraccionDbDto).filter_by(id=str(id)).one()
        return self.fabrica_interaccion.crear_objeto(
            interaccion_dto, MapeadorInteraccion()
        )

    def obtener_todos(self) -> list[Interaccion]:
        raise NotImplementedError

    def agregar(self, interaccion: Interaccion):
        interaccion_dto = self.fabrica_interaccion.crear_objeto(
            interaccion, MapeadorInteraccion()
        )
        db.session.add(interaccion_dto)

    def actualizar(self, interaccion: Interaccion):
        # TODO
        raise NotImplementedError

    def eliminar(self, interaccion_id: UUID):
        # TODO
        raise NotImplementedError
