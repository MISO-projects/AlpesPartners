from dataclasses import dataclass
import uuid
from marketing.seedwork.dominio.eventos import EventoDominio
from decimal import Decimal
from enum import Enum
from datetime import datetime
import uuid
from dataclasses import field


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


@dataclass
class ComisionReservada(EventoDominio):
    id_correlacion: str = None
    id_comision: uuid.UUID = None
    id_interaccion: uuid.UUID = None
    id_campania: uuid.UUID = None
    monto: MontoComision = None
    configuracion: ConfiguracionComision = None
    timestamp: datetime = None
    politica_fraude: PoliticaFraude = None
    fraud_ok: bool = None
    score_fraude: int = None


@dataclass
class ComisionRevertida(EventoDominio):
    id_comision: uuid.UUID = None
    journey_id: uuid.UUID = None
    monto_revertido: MontoComision = None
    motivo: str = None
    fecha_reversion: datetime = None


@dataclass
class FraudeDetectado(EventoDominio):
    journey_id: uuid.UUID = None
