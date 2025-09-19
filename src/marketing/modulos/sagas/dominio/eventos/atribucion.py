from dataclasses import dataclass
import uuid
from decimal import Decimal
from dataclasses import field

from marketing.seedwork.dominio.eventos import EventoDominio


@dataclass
class AtribucionRevertida(EventoDominio):
    journey_id_revertido: uuid.UUID = None
    interacciones: list[uuid.UUID] = field(default_factory=list)


@dataclass(frozen=True)
class MontoComision:
    valor: Decimal
    moneda: str = field(default="USD")

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El monto de comisión no puede ser negativo")
        if not self.moneda:
            raise ValueError("La moneda es requerida")


@dataclass
class ConversionAtribuida(EventoDominio):
    id_interaccion_atribuida: uuid.UUID = None
    id_campania: uuid.UUID = None
    id_afiliado: uuid.UUID = None
    tipo_conversion: str = None
    monto_atribuido: MontoComision = None
    id_interaccion_original: uuid.UUID = None
    score_fraude: int = None
