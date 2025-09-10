from uuid import UUID
from tracking.modulos.interacciones.dominio.repositorios import RepositorioInteraccion
from tracking.modulos.interacciones.dominio.fabricas import FabricaInteraccion
from tracking.modulos.interacciones.dominio.entidades import Interaccion
from tracking.modulos.interacciones.infraestructura.mapeadores import (
    MapeadorInteraccionSQLite,
    MapeadorInteraccionMongoDB,
)
from tracking.modulos.interacciones.infraestructura.dto import InteraccionDbDto
from tracking.config.db import db
from tracking.config.mongo import mongo_config


class RepositorioInteraccionSQLite(RepositorioInteraccion):
    def __init__(self):
        self._fabrica_interaccion: FabricaInteraccion = FabricaInteraccion()

    @property
    def fabrica_interaccion(self) -> FabricaInteraccion:
        return self._fabrica_interaccion

    def obtener_por_id(self, id: UUID) -> Interaccion:
        interaccion_dto = db.session.query(InteraccionDbDto).filter_by(id=str(id)).one()
        return self.fabrica_interaccion.crear_objeto(
            interaccion_dto, MapeadorInteraccionSQLite()
        )

    def obtener_todos(self) -> list[Interaccion]:
        raise NotImplementedError

    def agregar(self, interaccion: Interaccion):
        interaccion_dto = self.fabrica_interaccion.crear_objeto(
            interaccion, MapeadorInteraccionSQLite()
        )
        db.session.add(interaccion_dto)

    def actualizar(self, interaccion: Interaccion):
        # TODO
        raise NotImplementedError

    def eliminar(self, interaccion_id: UUID):
        # TODO
        raise NotImplementedError


class RepositorioInteraccionMongoDB(RepositorioInteraccion):
    def __init__(self):
        self._fabrica_interaccion: FabricaInteraccion = FabricaInteraccion()

    @property
    def fabrica_interaccion(self) -> FabricaInteraccion:
        return self._fabrica_interaccion

    def _get_collection(self):
        """Get collection reference when needed - don't store it"""
        return mongo_config.get_database()['interacciones']

    def obtener_por_id(self, id: UUID) -> Interaccion:
        collection = self._get_collection()
        document = collection.find_one({"_id": str(id)})
        if not document:
            raise ValueError(f"Interacción con ID {id} no encontrada")

        return self.fabrica_interaccion.crear_objeto(
            document, MapeadorInteraccionMongoDB()
        )

    def obtener_todos(self) -> list[Interaccion]:
        collection = self._get_collection()
        documents = list(collection.find())
        return [
            self.fabrica_interaccion.crear_objeto(doc, MapeadorInteraccionMongoDB())
            for doc in documents
        ]

    def agregar(self, interaccion: Interaccion):
        collection = self._get_collection()
        document = self.fabrica_interaccion.crear_objeto(
            interaccion, MapeadorInteraccionMongoDB()
        )
        collection.insert_one(document)

    def actualizar(self, interaccion: Interaccion):
        collection = self._get_collection()
        document = self.fabrica_interaccion.crear_objeto(
            interaccion, MapeadorInteraccionMongoDB()
        )
        collection.replace_one({"_id": str(interaccion.id)}, document)

    def eliminar(self, interaccion_id: UUID):
        collection = self._get_collection()
        result = collection.delete_one({"_id": str(interaccion_id)})
        if result.deleted_count == 0:
            raise ValueError(f"Interacción con ID {interaccion_id} no encontrada")
