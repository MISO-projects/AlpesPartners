from uuid import UUID
from atribucion.config.db import db
from atribucion.config.mongo import mongo_config
from atribucion.modulos.atribucion.dominio.entidades import Journey
from atribucion.modulos.atribucion.dominio.fabricas import FabricaAtribucion
from atribucion.modulos.atribucion.dominio.repositorios import RepositorioJourney
from .dto import Journey as JourneyDTO
from .mapeadores import MapeadorJourneySQLite, MapeadorJourneyMongoDB

class RepositorioJourneySQLite(RepositorioJourney):
    def __init__(self):
        self._fabrica_atribucion: FabricaAtribucion = FabricaAtribucion()

    @property
    def fabrica_atribucion(self) -> FabricaAtribucion:
        return self._fabrica_atribucion

    def obtener_por_id(self, id: UUID) -> Journey:
        journey_dto = db.session.query(JourneyDTO).filter_by(id=str(id)).one()
        return self.fabrica_atribucion.crear_objeto(
            journey_dto, MapeadorJourneySQLite()
        )

    def obtener_por_usuario(self, usuario_id: str) -> Journey:
        journey_dto = db.session.query(JourneyDTO).filter_by(usuario_id=usuario_id).first()
        if not journey_dto:
            return None
        return self.fabrica_atribucion.crear_objeto(
            journey_dto, MapeadorJourneySQLite()
        )

    def obtener_todos(self) -> list[Journey]:
        journey_dtos = db.session.query(JourneyDTO).all()
        return [
            self.fabrica_atribucion.crear_objeto(dto, MapeadorJourneySQLite())
            for dto in journey_dtos
        ]

    def agregar(self, journey: Journey):
        journey_dto = self.fabrica_atribucion.crear_objeto(
            journey, MapeadorJourneySQLite()
        )
        db.session.add(journey_dto)

    def actualizar(self, journey: Journey):
        journey_dto = self.fabrica_atribucion.crear_objeto(
            journey, MapeadorJourneySQLite()
        )
        db.session.merge(journey_dto)

    def eliminar(self, journey_id: UUID):
        result = db.session.query(JourneyDTO).filter_by(id=str(journey_id)).delete()
        if result == 0:
            raise ValueError(f"Journey con ID {journey_id} no encontrado")


class RepositorioJourneyMongoDB(RepositorioJourney):
    def __init__(self):
        self._fabrica_atribucion: FabricaAtribucion = FabricaAtribucion()

    @property
    def fabrica_atribucion(self) -> FabricaAtribucion:
        return self._fabrica_atribucion
        
    def _get_collection(self):
        # ¡CAMBIO 2! Usamos el método .get_database() del objeto importado
        return mongo_config.get_database()['journeys']

    def obtener_por_id(self, id: UUID) -> Journey:
        collection = self._get_collection()
        document = collection.find_one({"_id": str(id)})
        if not document:
            raise ValueError(f"Journey con ID {id} no encontrado")
        return self.fabrica_atribucion.crear_objeto(document, MapeadorJourneyMongoDB())

    def obtener_por_usuario(self, usuario_id: str) -> Journey:
        collection = self._get_collection()
        document = collection.find_one({"usuario_id": usuario_id})
        if not document:
            return None
        return self.fabrica_atribucion.crear_objeto(document, MapeadorJourneyMongoDB())

    def obtener_todos(self) -> list[Journey]:
        collection = self._get_collection()
        documents = list(collection.find())
        return [
            self.fabrica_atribucion.crear_objeto(doc, MapeadorJourneyMongoDB())
            for doc in documents
        ]

    def agregar(self, journey: Journey):
        collection = self._get_collection()
        document = self.fabrica_atribucion.crear_objeto(journey, MapeadorJourneyMongoDB())
        collection.insert_one(document)

    def actualizar(self, journey: Journey):
        collection = self._get_collection()
        document = self.fabrica_atribucion.crear_objeto(journey, MapeadorJourneyMongoDB())
        collection.replace_one({"_id": str(journey.id)}, document, upsert=True)

    def eliminar(self, journey_id: UUID):
        collection = self._get_collection()
        result = collection.delete_one({"_id": str(journey_id)})
        if result.deleted_count == 0:
            raise ValueError(f"Journey con ID {journey_id} no encontrado")