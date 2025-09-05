from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import uuid
from alpespartners.seedwork.dominio.eventos import EventoDominio
from alpespartners.modulos.marketing.dominio.objetos_valor import SegmentoAudiencia


@dataclass
class CampaniaCreada(EventoDominio):
    id_campania: uuid.UUID = None
    nombre: str = None
    tipo: str = None
    fecha_inicio: datetime = None
    fecha_fin: datetime = None
    segmento: SegmentoAudiencia = None


@dataclass
class CampaniaActivada(EventoDominio):
    id_campania: uuid.UUID = None
    nombre: str = None
    fecha_activacion: datetime = None


@dataclass
class CampaniaDesactivada(EventoDominio):
    id_campania: uuid.UUID = None
    razon: str = None


@dataclass
class InteraccionRecibida(EventoDominio):
    id_campania: uuid.UUID = None
    tipo_interaccion: str = None
    parametros_tracking: dict = None
    timestamp: datetime = None


@dataclass
class CampaniaCompletada(EventoDominio):
    id_campania: uuid.UUID = None
    fecha_completado: datetime = None
    metricas_finales: dict = None
