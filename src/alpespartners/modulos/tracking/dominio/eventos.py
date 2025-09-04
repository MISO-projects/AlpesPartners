from __future__ import annotations
from dataclasses import dataclass, field
from alpespartners.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
from alpespartners.modulos.tracking.dominio.objetos_valor import (
    IdentidadUsuario,
    ParametrosTracking,
    ElementoObjetivo,
    ContextoInteraccion,
)
import uuid


@dataclass
class InteraccionRegistrada(EventoDominio):
    id_interaccion: uuid.UUID = None
    tipo: str = None
    marca_temporal: datetime = None
    identidad_usuario: IdentidadUsuario = None
    parametros_tracking: ParametrosTracking = None
    elemento_objetivo: ElementoObjetivo = None
    contexto: ContextoInteraccion = None
