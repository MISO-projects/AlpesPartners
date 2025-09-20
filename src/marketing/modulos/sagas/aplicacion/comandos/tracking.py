from marketing.seedwork.aplicacion.comandos import Comando, ComandoHandler
from dataclasses import dataclass
import uuid
from marketing.modulos.sagas.aplicacion.dto.interaccion import (
    IdentidadUsuarioDTO,
    ParametrosTrackingDTO,
    ElementoObjetivoDTO,
    ContextoInteraccionDTO,
)
from datetime import datetime
from marketing.seedwork.aplicacion.comandos import ejecutar_commando as comando
from marketing.modulos.sagas.infraestructura.despachadores import (
    DespachadorSagas,
)


@dataclass
class RegistrarInteraccion(Comando):
    tipo: str
    marca_temporal: datetime
    identidad_usuario: IdentidadUsuarioDTO
    parametros_tracking: ParametrosTrackingDTO
    elemento_objetivo: ElementoObjetivoDTO
    contexto: ContextoInteraccionDTO


@dataclass
class DescartarInteracciones(Comando):
    id_correlacion: str
    interacciones: list[uuid.UUID]


class DescartarInteraccionesHandler(ComandoHandler):
    def handle(self, comando: DescartarInteracciones):
        despachador = DespachadorSagas()
        despachador.publicar_comando_descartar_interacciones(comando)


@comando.register(DescartarInteracciones)
def ejecutar_comando(comando: DescartarInteracciones):
    handler = DescartarInteraccionesHandler()
    return handler.handle(comando)
