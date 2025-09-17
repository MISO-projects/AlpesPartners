from marketing.seedwork.aplicacion.comandos import Comando
from dataclasses import dataclass
import uuid
from marketing.modulos.sagas.aplicacion.dto.atribucion import AtribucionDTO


@dataclass
class RegistrarAtribucion(Comando):
    atribucion: AtribucionDTO


@dataclass
class RevertirAtribucion(Comando):
    id_interaccion: uuid.UUID
