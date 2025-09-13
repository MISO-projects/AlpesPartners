# src/attribution/modulos/attribution/dominio/objetos_valor.py
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from atribucion.seedwork.dominio.objetos_valor import ObjetoValor
from datetime import datetime
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .entidades import Touchpoint, TipoModeloAtribucion

@dataclass(frozen=True)
class MontoComision(ObjetoValor):
    valor: Decimal
    moneda: str = field(default="USD")

@dataclass(frozen=True)
class ScoreFraude(ObjetoValor):
    valor: int

@dataclass(frozen=True)
class ConfiguracionAtribucion(ObjetoValor):
    """Objeto Valor que contiene los parámetros para los modelos de atribución."""
   
    factor_decaimiento: float = 7.0
    peso_primer_touch: float = 0.4
    peso_ultimo_touch: float = 0.4
    
    @property
    def peso_touch_intermedio(self) -> float:
        # Calculado para asegurar que siempre sume 1.0
        return 1.0 - (self.peso_primer_touch + self.peso_ultimo_touch)

    def es_valida(self) -> bool:
        # Regla de negocio: los pesos deben sumar 100%
        total = self.peso_primer_touch + self.peso_ultimo_touch + self.peso_touch_intermedio
        return abs(total - 1.0) < 0.01

@dataclass(frozen=True)
class AtribucionCalculada(ObjetoValor):
    """Objeto Valor que representa el resultado final de un cálculo de atribución."""
    touchpoint: 'Touchpoint'
    peso_atribucion: float 
    valor_atribuido: float
    modelo_usado: 'TipoModeloAtribucion'
    fecha_calculo: datetime = field(default_factory=datetime.now)

    def porcentaje_atribucion(self) -> float:
        return self.peso_atribucion * 100

class TipoInteraccion(str, Enum):
    CLICK = "click"
    VIEW = "view" 
    CONVERSION = "conversion"

@dataclass(frozen=True)
class IdentificadorUniversal(ObjetoValor):
    """UUID wrapper genérico."""
    valor: uuid.UUID
    
    @classmethod
    def generar(cls) -> IdentificadorUniversal:
        return cls(uuid.uuid4())