from marketing.seedwork.aplicacion.comandos import Comando
from dataclasses import dataclass
import uuid
from marketing.modulos.sagas.aplicacion.dto.interaccion import (
    IdentidadUsuarioDTO,
    ParametrosTrackingDTO,
    ElementoObjetivoDTO,
    ContextoInteraccionDTO,
)
from datetime import datetime


@dataclass
class RegistrarInteraccion(Comando):
    tipo: str
    marca_temporal: datetime
    identidad_usuario: IdentidadUsuarioDTO
    parametros_tracking: ParametrosTrackingDTO
    elemento_objetivo: ElementoObjetivoDTO
    contexto: ContextoInteraccionDTO


class DescartarInteraccion(Comando):
    id_interaccion: uuid.UUID
