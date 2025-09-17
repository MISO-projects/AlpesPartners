from dataclasses import dataclass
import uuid
from marketing.seedwork.dominio.eventos import EventoDominio


@dataclass
class ComisionRevertida(EventoDominio):
    id_interaccion: uuid.UUID = None



@dataclass
class FraudeDetectado(EventoDominio):
    id_interaccion: uuid.UUID = None