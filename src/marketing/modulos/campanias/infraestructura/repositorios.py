from uuid import UUID
from marketing.modulos.campanias.dominio.repositorios import RepositorioCampania
from marketing.modulos.campanias.dominio.fabricas import FabricaCampania
from marketing.modulos.campanias.dominio.entidades import Campania, EstadoCampania
from marketing.modulos.campanias.infraestructura.mapeadores import MapeadorCampaniaSQLite, MapeadorCampaniaMongoDB
from marketing.modulos.campanias.infraestructura.dto import CampaniaDbDto
from marketing.config.db import db
from marketing.config.mongo import mongo_config


class RepositorioCampaniaSQLite(RepositorioCampania):
    def __init__(self):
        self._fabrica_campania: FabricaCampania = FabricaCampania()

    @property
    def fabrica_campania(self) -> FabricaCampania:
        return self._fabrica_campania

    def obtener_por_id(self, id: UUID) -> Campania:
        campania_dto = db.session.query(CampaniaDbDto).filter_by(id=str(id)).one()
        return self.fabrica_campania.crear_objeto(campania_dto, MapeadorCampaniaSQLite())

    def obtener_por_nombre(self, nombre: str) -> Campania:
        campania_dto = db.session.query(CampaniaDbDto).filter_by(nombre=nombre).first()
        if campania_dto:
            return self.fabrica_campania.crear_objeto(campania_dto, MapeadorCampaniaSQLite())
        return None

    def obtener_activas(self) -> list[Campania]:
        campanias_dto = db.session.query(CampaniaDbDto).filter_by(estado=EstadoCampania.ACTIVA.value).all()
        return [
            self.fabrica_campania.crear_objeto(dto, MapeadorCampaniaSQLite()) 
            for dto in campanias_dto
        ]

    def obtener_por_segmento(self, ubicacion: str = None, edad_minima: int = None, edad_maxima: int = None) -> list[Campania]:
        campanias_dto = db.session.query(CampaniaDbDto).filter_by(estado=EstadoCampania.ACTIVA.value).all()
        
        result = []
        for dto in campanias_dto:
            segmento = dto.segmento or {}
            if ubicacion and segmento.get('ubicacion') != ubicacion:
                continue
            if edad_minima and segmento.get('edad_minima', 0) > edad_minima:
                continue
            if edad_maxima and segmento.get('edad_maxima', 100) < edad_maxima:
                continue
            
            campania = self.fabrica_campania.crear_objeto(dto, MapeadorCampaniaSQLite())
            result.append(campania)
        
        return result

    def obtener_todos(self) -> list[Campania]:
        campanias_dto = db.session.query(CampaniaDbDto).all()
        return [
            self.fabrica_campania.crear_objeto(dto, MapeadorCampaniaSQLite()) 
            for dto in campanias_dto
        ]

    def agregar(self, campania: Campania):
        campania_dto = self.fabrica_campania.crear_objeto(campania, MapeadorCampaniaSQLite())
        db.session.add(campania_dto)

    def actualizar(self, campania: Campania):
        campania_dto = self.fabrica_campania.crear_objeto(campania, MapeadorCampaniaSQLite())
        db.session.merge(campania_dto)

    def eliminar(self, campania_id: UUID):
        campania_dto = db.session.query(CampaniaDbDto).filter_by(id=str(campania_id)).first()
        if campania_dto:
            db.session.delete(campania_dto)


class RepositorioCampaniaMongoDB(RepositorioCampania):
    def __init__(self):
        self._fabrica_campania: FabricaCampania = FabricaCampania()

    @property
    def fabrica_campania(self) -> FabricaCampania:
        return self._fabrica_campania
    
    def _get_collection(self):
        """Get collection reference when needed - don't store it to avoid pickle issues"""
        return mongo_config.get_database()['campanias']

    def obtener_por_id(self, id: UUID) -> Campania:
        collection = self._get_collection()
        document = collection.find_one({"_id": str(id)})
        if not document:
            raise ValueError(f"Campaña con ID {id} no encontrada")
        
        return self.fabrica_campania.crear_objeto(
            document, MapeadorCampaniaMongoDB()
        )

    def obtener_por_nombre(self, nombre: str) -> Campania:
        collection = self._get_collection()
        document = collection.find_one({"nombre": nombre})
        if not document:
            return None
        
        return self.fabrica_campania.crear_objeto(
            document, MapeadorCampaniaMongoDB()
        )

    def obtener_activas(self) -> list[Campania]:
        collection = self._get_collection()
        documents = list(collection.find({"estado": EstadoCampania.ACTIVA.value}))
        return [
            self.fabrica_campania.crear_objeto(doc, MapeadorCampaniaMongoDB())
            for doc in documents
        ]

    def obtener_por_segmento(self, ubicacion: str = None, edad_minima: int = None, edad_maxima: int = None) -> list[Campania]:
        collection = self._get_collection()
        
        # Build MongoDB query for segment filtering
        query = {"estado": EstadoCampania.ACTIVA.value}
        
        if ubicacion:
            query["segmento.ubicacion"] = ubicacion
        
        if edad_minima is not None:
            query["segmento.edad_minima"] = {"$lte": edad_minima}
        
        if edad_maxima is not None:
            query["segmento.edad_maxima"] = {"$gte": edad_maxima}
        
        documents = list(collection.find(query))
        return [
            self.fabrica_campania.crear_objeto(doc, MapeadorCampaniaMongoDB())
            for doc in documents
        ]

    def obtener_todos(self) -> list[Campania]:
        collection = self._get_collection()
        documents = list(collection.find())
        return [
            self.fabrica_campania.crear_objeto(doc, MapeadorCampaniaMongoDB())
            for doc in documents
        ]

    def agregar(self, campania: Campania):
        collection = self._get_collection()
        document = self.fabrica_campania.crear_objeto(
            campania, MapeadorCampaniaMongoDB()
        )
        collection.insert_one(document)

    def actualizar(self, campania: Campania):
        collection = self._get_collection()
        document = self.fabrica_campania.crear_objeto(
            campania, MapeadorCampaniaMongoDB()
        )
        collection.replace_one({"_id": str(campania.id)}, document)

    def eliminar(self, campania_id: UUID):
        collection = self._get_collection()
        result = collection.delete_one({"_id": str(campania_id)})
        if result.deleted_count == 0:
            raise ValueError(f"Campaña con ID {campania_id} no encontrada") 