from __future__ import annotations
from dataclasses import dataclass, field
from tracking.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
from tracking.modulos.interacciones.dominio.objetos_valor import (
    IdentidadUsuario,
    ParametrosTracking,
    ElementoObjetivo,
    ContextoInteraccion,
)
import uuid


@dataclass
class InteraccionRegistrada(EventoDominio):
    id_correlacion: str = None
    id_interaccion: uuid.UUID = None
    tipo: str = None
    marca_temporal: datetime = None
    identidad_usuario: IdentidadUsuario = None
    parametros_tracking: ParametrosTracking = None
    elemento_objetivo: ElementoObjetivo = None
    contexto: ContextoInteraccion = None
    estado: str = None

@dataclass
class InteraccionDescartada(EventoDominio):
    id_interaccion: uuid.UUID = None
    tipo: str = None
    marca_temporal: datetime = None
    identidad_usuario: IdentidadUsuario = None
    parametros_tracking: ParametrosTracking = None
    elemento_objetivo: ElementoObjetivo = None
    contexto: ContextoInteraccion = None
    estado: str = None


@dataclass
class InteraccionesDescartadas(EventoDominio):
    id_correlacion: str = None
    interacciones: list[uuid.UUID] = None
