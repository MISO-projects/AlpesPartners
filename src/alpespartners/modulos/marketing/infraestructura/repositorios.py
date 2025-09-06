from uuid import UUID
from alpespartners.modulos.marketing.dominio.repositorios import RepositorioCampania
from alpespartners.modulos.marketing.dominio.fabricas import FabricaCampania
from alpespartners.modulos.marketing.dominio.entidades import Campania, EstadoCampania
from alpespartners.modulos.marketing.infraestructura.mapeadores import MapeadorCampania
from alpespartners.modulos.marketing.infraestructura.dto import CampaniaDbDto
from alpespartners.config.db import db
from alpespartners.seedwork.dominio.entidades import Entidad


class RepositorioCampaniaSQLite(RepositorioCampania):
    def __init__(self):
        self._fabrica_campania: FabricaCampania = FabricaCampania()

    @property
    def fabrica_campania(self) -> FabricaCampania:
        return self._fabrica_campania

    def obtener_por_id(self, id: UUID) -> Campania:
        campania_dto = db.session.query(CampaniaDbDto).filter_by(id=str(id)).one()
        return self.fabrica_campania.crear_objeto(campania_dto, MapeadorCampania())

    def obtener_por_nombre(self, nombre: str) -> Campania:
        campania_dto = db.session.query(CampaniaDbDto).filter_by(nombre=nombre).first()
        if campania_dto:
            return self.fabrica_campania.crear_objeto(campania_dto, MapeadorCampania())
        return None

    def obtener_activas(self) -> list[Campania]:
        campanias_dto = db.session.query(CampaniaDbDto).filter_by(estado=EstadoCampania.ACTIVA.value).all()
        return [
            self.fabrica_campania.crear_objeto(dto, MapeadorCampania()) 
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
            
            campania = self.fabrica_campania.crear_objeto(dto, MapeadorCampania())
            result.append(campania)
        
        return result

    def obtener_todos(self) -> list[Campania]:
        campanias_dto = db.session.query(CampaniaDbDto).all()
        return [
            self.fabrica_campania.crear_objeto(dto, MapeadorCampania()) 
            for dto in campanias_dto
        ]

    def agregar(self, campania: Campania):
        campania_dto = self.fabrica_campania.crear_objeto(campania, MapeadorCampania())
        db.session.add(campania_dto)

    def actualizar(self, campania: Campania):
        campania_dto = self.fabrica_campania.crear_objeto(campania, MapeadorCampania())
        db.session.merge(campania_dto)

    def eliminar(self, campania_id: UUID):
        campania_dto = db.session.query(CampaniaDbDto).filter_by(id=str(campania_id)).first()
        if campania_dto:
            db.session.delete(campania_dto)
