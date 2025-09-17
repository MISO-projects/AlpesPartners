from marketing.seedwork.aplicacion.comandos import Comando
from dataclasses import dataclass
import uuid


@dataclass
class RevertirAtribucion(Comando):
    id_interaccion: uuid.UUID
