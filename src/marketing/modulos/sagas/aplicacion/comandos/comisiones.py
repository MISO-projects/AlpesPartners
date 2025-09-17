from marketing.seedwork.aplicacion.comandos import Comando
from dataclasses import dataclass
import uuid

@dataclass
class RevertirComision(Comando):
    id_interaccion: uuid.UUID
