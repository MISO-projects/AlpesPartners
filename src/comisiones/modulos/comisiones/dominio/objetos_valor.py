from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from datetime import datetime
import uuid

class TipoComision(Enum):
    PORCENTAJE = "PORCENTAJE"
    FIJO = "FIJO"
    ESCALONADO = "ESCALONADO"

class EstadoComision(Enum):
    RESERVADA = "RESERVADA"
    CONFIRMADA = "CONFIRMADA"
    REVERTIDA = "REVERTIDA"
    CANCELADA = "CANCELADA"

class TipoPoliticaFraude(Enum):
    STRICT = "STRICT"
    MODERATE = "MODERATE"
    PERMISSIVE = "PERMISSIVE"

@dataclass(frozen=True)
class MontoComision:
    valor: Decimal
    moneda: str = field(default="USD")
    
    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El monto de comisión no puede ser negativo")
        if not self.moneda:
            raise ValueError("La moneda es requerida")

@dataclass(frozen=True)
class ConfiguracionComision:
    tipo: TipoComision
    porcentaje: Decimal = field(default=Decimal('0'))
    monto_fijo: MontoComision = field(default=None)
    escalones: list = field(default_factory=list)
    minimo: MontoComision = field(default=None)
    maximo: MontoComision = field(default=None)
    
    def __post_init__(self):
        if self.tipo == TipoComision.PORCENTAJE and self.porcentaje <= 0:
            raise ValueError("El porcentaje debe ser mayor a 0")
        if self.tipo == TipoComision.FIJO and not self.monto_fijo:
            raise ValueError("Monto fijo es requerido para comisiones fijas")

@dataclass(frozen=True)
class PoliticaFraude:
    tipo: TipoPoliticaFraude
    threshold_score: int = field(default=50)
    requiere_revision_manual: bool = field(default=False)
    tiempo_espera_minutos: int = field(default=0)
    
    def __post_init__(self):
        if not (0 <= self.threshold_score <= 100):
            raise ValueError("El threshold debe estar entre 0 y 100")

@dataclass(frozen=True)
class InteraccionAtribuida:
    id_interaccion: uuid.UUID
    id_campania: uuid.UUID
    tipo_interaccion: str
    valor_interaccion: MontoComision
    fraud_ok: bool
    score_fraude: int = field(default=0)
    timestamp: datetime = field(default_factory=datetime.now)
    parametros_adicionales: dict = field(default_factory=dict)

@dataclass(frozen=True)
class DetallesReserva:
    id_comision: uuid.UUID
    monto_reservado: MontoComision
    fecha_reserva: datetime
    referencia_interaccion: uuid.UUID
    motivo: str = field(default="")
    metadata: dict = field(default_factory=dict)

@dataclass(frozen=True)
class DetallesConfirmacion:
    fecha_confirmacion: datetime
    monto_confirmado: MontoComision
    lote_confirmacion: str = field(default="")
    referencia_pago: str = field(default="")
    metadata: dict = field(default_factory=dict)
