from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid
from atribucion.seedwork.dominio.eventos import EventoDominio
from atribucion.modulos.atribucion.dominio.objetos_valor import MontoComision


@dataclass
class InteraccionAtribuidaRecibida(EventoDominio):
    """Evento que indica que una interacción fue atribuida exitosamente a una campaña"""
    
    id_interaccion: str = field(default="")
    id_campania: str = field(default="") 
    tipo_interaccion: str = field(default="CLICK")
    valor_interaccion: MontoComision = field(default_factory=MontoComision)
    fraud_ok: bool = field(default=True)
    score_fraude: int = field(default=0)
    timestamp: datetime = field(default_factory=datetime.now)