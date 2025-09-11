from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from atribucion.seedwork.dominio.objetos_valor import ObjetoValor
from datetime import datetime
import uuid


@dataclass(frozen=True)
class MontoComision:
    """VO compatible con el servicio de Comisiones"""
    valor: Decimal
    moneda: str = field(default="USD")
    
    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El monto de comisión no puede ser negativo")
        if not self.moneda:
            raise ValueError("La moneda es requerida")


class TipoInteraccion(str, Enum):
    """Tipos de interacción soportados en atribución"""
    CLICK = "click"
    VIEW = "view" 
    CONVERSION = "conversion"
    INSTALL = "install"
    PURCHASE = "purchase"


@dataclass(frozen=True)
class ScoreFraude(ObjetoValor):
    """Score de fraude (0-100) con validación"""
    valor: int
    
    def __post_init__(self):
        if not 0 <= self.valor <= 100:
            raise ValueError("El score de fraude debe estar entre 0 y 100")
    
    @property
    def es_fraudulento(self) -> bool:
        """Considera fraudulento si el score es mayor a 70"""
        return self.valor > 70
    
    @property
    def es_sospechoso(self) -> bool:
        """Considera sospechoso si el score está entre 50 y 70"""
        return 50 <= self.valor <= 70


@dataclass(frozen=True)
class IdentificadorInteraccion(ObjetoValor):
    """UUID wrapper para identificadores de interacción"""
    valor: uuid.UUID
    
    @classmethod
    def generar(cls) -> IdentificadorInteraccion:
        return cls(uuid.uuid4())
    
    @classmethod
    def desde_string(cls, id_str: str) -> IdentificadorInteraccion:
        return cls(uuid.UUID(id_str))
    
    def __str__(self) -> str:
        return str(self.valor)


@dataclass(frozen=True)
class IdentificadorCampania(ObjetoValor):
    """UUID wrapper para identificadores de campaña"""
    valor: uuid.UUID
    
    @classmethod
    def desde_string(cls, id_str: str) -> IdentificadorCampania:
        return cls(uuid.UUID(id_str))
    
    def __str__(self) -> str:
        return str(self.valor)