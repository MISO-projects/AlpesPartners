
from seedwork.aplicacion.comandos import Comando, ComandoHandler, ejecutar_commando as comando
from modulos.comisiones.dominio.repositorios import RepositorioComision
from modulos.comisiones.dominio.excepciones import ComisionNoEncontradaExcepcion
from modulos.comisiones.infraestructura.fabricas import FabricaRepositorio
from seedwork.infraestructura.uow import UnidadTrabajoPuerto
from dataclasses import dataclass
import uuid

@dataclass
class RevertirComision(Comando):

    id_comision: uuid.UUID
    motivo: str = ""

class RevertirComisionHandler(ComandoHandler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

    def handle(self, comando: RevertirComision):

        try:
            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )
            comision = repositorio.obtener_por_id(comando.id_comision)
            if not comision:
                raise ComisionNoEncontradaExcepcion(f"Comisión {comando.id_comision} no encontrada")
            comision.revertir_comision(motivo=comando.motivo)
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, comision)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

            print(f"Comisión {comision.id} revertida exitosamente. Motivo: {comando.motivo}")
            return comision

        except Exception as e:
            UnidadTrabajoPuerto.rollback()
            print(f"Error revirtiendo comisión: {e}")
            raise e

@comando.register(RevertirComision)
def ejecutar_comando(comando: RevertirComision):
    handler = RevertirComisionHandler()
    return handler.handle(comando)
