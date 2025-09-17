from marketing.seedwork.aplicacion.comandos import Comando
from dataclasses import dataclass
import uuid
from decimal import Decimal


@dataclass
class ReservarComision(Comando):

    id_interaccion: uuid.UUID
    id_campania: uuid.UUID
    tipo_interaccion: str
    valor_interaccion: Decimal
    moneda_interaccion: str = "USD"
    fraud_ok: bool = True
    score_fraude: int = 0
    parametros_adicionales: dict = None


@dataclass
class RevertirComision(Comando):
    id_interaccion: uuid.UUID
