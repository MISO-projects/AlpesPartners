from tracking.seedwork.aplicacion.comandos import Comando
from tracking.modulos.interacciones.aplicacion.comandos.base import (
    ComandoInteraccionBaseHandler,
)
from dataclasses import dataclass
import uuid
from tracking.modulos.interacciones.infraestructura.repositorios import (
    RepositorioInteraccion,
)
from tracking.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from tracking.seedwork.aplicacion.comandos import ejecutar_commando as comando
from tracking.modulos.interacciones.infraestructura.despachadores import DespachadorTracking
from tracking.modulos.interacciones.dominio.eventos import InteraccionesDescartadas


@dataclass
class DescartarInteracciones(Comando):
    id_correlacion: str
    interacciones: list[uuid.UUID]


class DescartarInteraccionesHandler(ComandoInteraccionBaseHandler):
    def handle(self, comando: DescartarInteracciones):
        try:
            print(f'Descartando interacciones: {comando.interacciones}')
            repositorio: RepositorioInteraccion = self.fabrica_repositorio.crear_objeto(
                RepositorioInteraccion.__class__
            )
            interacciones = repositorio.obtener_por_ids(comando.interacciones)
            for interaccion in interacciones:
                interaccion.descartar_interaccion(interaccion)
                UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, interaccion)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()
            despachador = DespachadorTracking()
            evento = InteraccionesDescartadas(
                id_correlacion=comando.id_correlacion,
                interacciones=comando.interacciones
            )
            despachador.publicar_evento_interacciones_descartadas(evento, 'interacciones-descartadas')
        except Exception as e:
            UnidadTrabajoPuerto.rollback()
            raise e


@comando.register(DescartarInteracciones)
def ejecutar_comando_descartar_interaccion(comando: DescartarInteracciones):
    handler = DescartarInteraccionesHandler()
    return handler.handle(comando)
