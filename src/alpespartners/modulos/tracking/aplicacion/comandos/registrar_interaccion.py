from alpespartners.seedwork.aplicacion.comandos import Comando, ComandoHandler
from alpespartners.modulos.tracking.aplicacion.comandos.base import (
    CrearInteraccionBaseHandler,
)
from alpespartners.modulos.tracking.aplicacion.dto import (
    IdentidadUsuarioDTO,
    ParametrosTrackingDTO,
    ElementoObjetivoDTO,
    ContextoInteraccionDTO,
)
from datetime import datetime

from alpespartners.modulos.tracking.aplicacion.dto import InteraccionDTO
from alpespartners.modulos.tracking.aplicacion.mapeadores import (
    MapeadorInteraccion,
)
from alpespartners.modulos.tracking.dominio.entidades import Interaccion
from alpespartners.modulos.tracking.infraestructura.repositorios import (
    RepositorioInteraccion,
)
from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando as comando
from dataclasses import dataclass


@dataclass
class RegistrarInteraccion(Comando):
    tipo: str
    marca_temporal: datetime
    identidad_usuario: IdentidadUsuarioDTO
    parametros_tracking: ParametrosTrackingDTO
    elemento_objetivo: ElementoObjetivoDTO
    contexto: ContextoInteraccionDTO


class RegistrarInteraccionHandler(CrearInteraccionBaseHandler):
    def handle(self, comando: RegistrarInteraccion):
        try:
            interaccion_dto = InteraccionDTO(
                tipo=comando.tipo,
                marca_temporal=comando.marca_temporal,
                identidad_usuario=comando.identidad_usuario,
                parametros_tracking=comando.parametros_tracking,
                elemento_objetivo=comando.elemento_objetivo,
                contexto=comando.contexto,
            )

            interaccion: Interaccion = self.fabrica_interaccion.crear_objeto(
                interaccion_dto, MapeadorInteraccion()
            )
            interaccion.registrar_interaccion(interaccion)
            repositorio = self.fabrica_repositorio.crear_objeto(
                RepositorioInteraccion.__class__
            )

            UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, interaccion)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()
        except Exception as e:
            UnidadTrabajoPuerto.rollback()
            raise e


@comando.register(RegistrarInteraccion)
def ejecutar_comando(comando: RegistrarInteraccion):
    handler = RegistrarInteraccionHandler()
    handler.handle(comando)
