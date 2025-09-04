from __future__ import annotations
from dataclasses import dataclass, field
from alpespartners.seedwork.dominio.eventos import EventoDominio
from datetime import datetime


@dataclass
class InteraccionRegistrada(EventoDominio):
    id_reserva: uuid.UUID = None
    codigo_error: str = None
    mensaje_error: str = None
    tiempo_procesamiento: int = None
    tiempo_total: int = None
    tiempo_total_ms: int = None
