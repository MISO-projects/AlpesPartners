
from uuid import UUID
from typing import List
from datetime import datetime
from modulos.comisiones.dominio.repositorios import (
    RepositorioComision,
    RepositorioConfiguracionComision,
    RepositorioPoliticaFraude
)
from modulos.comisiones.dominio.entidades import Comision
from modulos.comisiones.dominio.objetos_valor import (
    EstadoComision,
    ConfiguracionComision,
    PoliticaFraude,
    MontoComision,
    TipoComision,
    TipoPoliticaFraude
)
from modulos.comisiones.dominio.fabricas import (
    FabricaComision,
    FabricaConfiguracionComision,
    FabricaPoliticaFraude
)
from modulos.comisiones.infraestructura.dto import (
    ComisionDbDto,
    ConfiguracionComisionDbDto,
    PoliticaFraudeDbDto
)
from modulos.comisiones.infraestructura.mapeadores import (
    MapeadorComisionSQLite,
    MapeadorComisionMongoDB
)
from config.db import db
from config.mongo import mongo_config
from decimal import Decimal

class RepositorioComisionSQLite(RepositorioComision):

    def __init__(self):
        self._fabrica_comision = FabricaComision()

    @property
    def fabrica_comision(self) -> FabricaComision:
        return self._fabrica_comision

    def obtener_por_id(self, id: UUID) -> Comision:

        comision_dto = db.session.query(ComisionDbDto).filter_by(id=str(id)).one()
        return self.fabrica_comision.crear_objeto(comision_dto, MapeadorComisionSQLite())

    def obtener_por_interaccion(self, id_interaccion: UUID) -> Comision:

        comision_dto = db.session.query(ComisionDbDto).filter_by(id_interaccion=str(id_interaccion)).first()
        if comision_dto:
            return self.fabrica_comision.crear_objeto(comision_dto, MapeadorComisionSQLite())
        return None

    def obtener_por_campania(self, id_campania: UUID) -> List[Comision]:

        comisiones_dto = db.session.query(ComisionDbDto).filter_by(id_campania=str(id_campania)).all()
        return [
            self.fabrica_comision.crear_objeto(dto, MapeadorComisionSQLite())
            for dto in comisiones_dto
        ]

    def obtener_por_estado(self, estado: EstadoComision) -> List[Comision]:

        comisiones_dto = db.session.query(ComisionDbDto).filter_by(estado=estado.value).all()
        return [
            self.fabrica_comision.crear_objeto(dto, MapeadorComisionSQLite())
            for dto in comisiones_dto
        ]

    def obtener_reservadas_vencidas(self, fecha_limite: datetime) -> List[Comision]:

        comisiones_dto = db.session.query(ComisionDbDto).filter(
            ComisionDbDto.estado == EstadoComision.RESERVADA.value,
            ComisionDbDto.fecha_vencimiento.is_not(None),
            ComisionDbDto.fecha_vencimiento < fecha_limite
        ).all()
        
        return [
            self.fabrica_comision.crear_objeto(dto, MapeadorComisionSQLite())
            for dto in comisiones_dto
        ]

    def obtener_para_lote(self, limite: int = 100) -> List[Comision]:

        comisiones_dto = db.session.query(ComisionDbDto).filter_by(
            estado=EstadoComision.RESERVADA.value
        ).limit(limite).all()
        
        return [
            self.fabrica_comision.crear_objeto(dto, MapeadorComisionSQLite())
            for dto in comisiones_dto
        ]

    def obtener_todos(self) -> List[Comision]:

        comisiones_dto = db.session.query(ComisionDbDto).all()
        return [
            self.fabrica_comision.crear_objeto(dto, MapeadorComisionSQLite())
            for dto in comisiones_dto
        ]

    def agregar(self, comision: Comision):

        comision_dto = self.fabrica_comision.crear_objeto(comision, MapeadorComisionSQLite())
        db.session.add(comision_dto)

    def actualizar(self, comision: Comision):

        comision_dto = self.fabrica_comision.crear_objeto(comision, MapeadorComisionSQLite())
        db.session.merge(comision_dto)

    def eliminar(self, comision_id: UUID):

        comision_dto = db.session.query(ComisionDbDto).filter_by(id=str(comision_id)).first()
        if comision_dto:
            db.session.delete(comision_dto)

class RepositorioComisionMongoDB(RepositorioComision):

    def __init__(self):
        self._fabrica_comision = FabricaComision()

    @property
    def fabrica_comision(self) -> FabricaComision:
        return self._fabrica_comision

    def _get_collection(self):

        return mongo_config.get_database()['comisiones']

    def obtener_por_id(self, id: UUID) -> Comision:

        collection = self._get_collection()
        document = collection.find_one({"_id": str(id)})
        if not document:
            raise ValueError(f"Comisión con ID {id} no encontrada")
        
        return self.fabrica_comision.crear_objeto(document, MapeadorComisionMongoDB())

    def obtener_por_interaccion(self, id_interaccion: UUID) -> Comision:

        collection = self._get_collection()
        document = collection.find_one({"id_interaccion": str(id_interaccion)})
        if not document:
            return None
        
        return self.fabrica_comision.crear_objeto(document, MapeadorComisionMongoDB())

    def obtener_por_campania(self, id_campania: UUID) -> List[Comision]:

        collection = self._get_collection()
        documents = list(collection.find({"id_campania": str(id_campania)}))
        return [
            self.fabrica_comision.crear_objeto(doc, MapeadorComisionMongoDB())
            for doc in documents
        ]

    def obtener_por_estado(self, estado: EstadoComision) -> List[Comision]:

        collection = self._get_collection()
        documents = list(collection.find({"estado": estado.value}))
        return [
            self.fabrica_comision.crear_objeto(doc, MapeadorComisionMongoDB())
            for doc in documents
        ]

    def obtener_reservadas_vencidas(self, fecha_limite: datetime) -> List[Comision]:

        collection = self._get_collection()
        documents = list(collection.find({
            "estado": EstadoComision.RESERVADA.value,
            "fecha_vencimiento": {"$ne": None, "$lt": fecha_limite}
        }))
        
        return [
            self.fabrica_comision.crear_objeto(doc, MapeadorComisionMongoDB())
            for doc in documents
        ]

    def obtener_para_lote(self, limite: int = 100) -> List[Comision]:

        collection = self._get_collection()
        documents = list(collection.find(
            {"estado": EstadoComision.RESERVADA.value}
        ).limit(limite))
        
        return [
            self.fabrica_comision.crear_objeto(doc, MapeadorComisionMongoDB())
            for doc in documents
        ]

    def obtener_todos(self) -> List[Comision]:

        collection = self._get_collection()
        documents = list(collection.find())
        return [
            self.fabrica_comision.crear_objeto(doc, MapeadorComisionMongoDB())
            for doc in documents
        ]

    def agregar(self, comision: Comision):

        collection = self._get_collection()
        document = self.fabrica_comision.crear_objeto(comision, MapeadorComisionMongoDB())
        collection.insert_one(document)

    def actualizar(self, comision: Comision):

        collection = self._get_collection()
        document = self.fabrica_comision.crear_objeto(comision, MapeadorComisionMongoDB())
        collection.replace_one({"_id": str(comision.id)}, document)

    def eliminar(self, comision_id: UUID):

        collection = self._get_collection()
        result = collection.delete_one({"_id": str(comision_id)})
        if result.deleted_count == 0:
            raise ValueError(f"Comisión con ID {comision_id} no encontrada")

class RepositorioConfiguracionComisionSQLite(RepositorioConfiguracionComision):

    def __init__(self):
        self._fabrica_configuracion = FabricaConfiguracionComision()

    def obtener_por_campania(self, id_campania: UUID) -> ConfiguracionComision:

        config_dto = db.session.query(ConfiguracionComisionDbDto).filter_by(
            id_campania=str(id_campania), 
            activo=True
        ).first()
        
        if config_dto:
            return self._dto_a_configuracion(config_dto)
        return None

    def obtener_por_tipo_interaccion(self, tipo_interaccion: str) -> ConfiguracionComision:

        config_dto = db.session.query(ConfiguracionComisionDbDto).filter_by(
            tipo_interaccion=tipo_interaccion,
            activo=True
        ).first()
        
        if config_dto:
            return self._dto_a_configuracion(config_dto)
        return None

    def obtener_default(self) -> ConfiguracionComision:
        return self._fabrica_configuracion.crear_configuracion_porcentaje(
            porcentaje=Decimal('5.0'),
            minimo=MontoComision(valor=Decimal('1.0'), moneda='USD'),
            maximo=MontoComision(valor=Decimal('1000.0'), moneda='USD')
        )

    def _dto_a_configuracion(self, dto: ConfiguracionComisionDbDto) -> ConfiguracionComision:

        monto_fijo = None
        if dto.monto_fijo_valor:
            monto_fijo = MontoComision(valor=dto.monto_fijo_valor, moneda=dto.monto_fijo_moneda)

        minimo = None
        if dto.minimo_valor:
            minimo = MontoComision(valor=dto.minimo_valor, moneda=dto.minimo_moneda)

        maximo = None
        if dto.maximo_valor:
            maximo = MontoComision(valor=dto.maximo_valor, moneda=dto.maximo_moneda)

        return ConfiguracionComision(
            tipo=TipoComision(dto.tipo),
            porcentaje=dto.porcentaje or Decimal('0'),
            monto_fijo=monto_fijo,
            escalones=dto.escalones or [],
            minimo=minimo,
            maximo=maximo
        )

class RepositorioPoliticaFraudeSQLite(RepositorioPoliticaFraude):

    def __init__(self):
        self._fabrica_politica = FabricaPoliticaFraude()

    def obtener_por_campania(self, id_campania: UUID) -> PoliticaFraude:

        politica_dto = db.session.query(PoliticaFraudeDbDto).filter_by(
            id_campania=str(id_campania),
            activo=True
        ).first()
        
        if politica_dto:
            return self._dto_a_politica(politica_dto)
        return None

    def obtener_default(self) -> PoliticaFraude:
        return self._fabrica_politica.crear_politica_moderada(threshold_score=50)

    def _dto_a_politica(self, dto: PoliticaFraudeDbDto) -> PoliticaFraude:

        return PoliticaFraude(
            tipo=TipoPoliticaFraude(dto.tipo),
            threshold_score=dto.threshold_score,
            requiere_revision_manual=dto.requiere_revision_manual,
            tiempo_espera_minutos=dto.tiempo_espera_minutos
        )
