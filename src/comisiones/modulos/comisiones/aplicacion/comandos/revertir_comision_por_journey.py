from dataclasses import dataclass
import uuid
from comisiones.seedwork.aplicacion.comandos import Comando, ComandoHandler, ejecutar_commando as comando
from comisiones.modulos.comisiones.dominio.repositorios import RepositorioComision
from comisiones.modulos.comisiones.infraestructura.fabricas import FabricaRepositorio
from comisiones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from comisiones.modulos.comisiones.dominio.excepciones import ComisionNoEncontradaExcepcion

@dataclass
class RevertirComisionPorJourney(Comando):
    journey_id: uuid.UUID
    motivo: str = ""

class RevertirComisionPorJourneyHandler(ComandoHandler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

    def handle(self, comando: RevertirComisionPorJourney):
        try:
            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )
            comision = repositorio.obtener_por_journey_id(comando.journey_id)
            if not comision:
                raise ComisionNoEncontradaExcepcion(f"Comisión con journey_id {comando.journey_id} no encontrada")
            
            comision.revertir_comision(motivo=comando.motivo)
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, comision)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

            print(f"Comisión {comision.id} revertida exitosamente por journey_id {comando.journey_id}. Motivo: {comando.motivo}")
            return comision

        except Exception as e:
            UnidadTrabajoPuerto.rollback()
            print(f"Error revirtiendo comisión por journey_id: {e}")
            raise e

@comando.register(RevertirComisionPorJourney)
def ejecutar_comando(comando: RevertirComisionPorJourney):
    handler = RevertirComisionPorJourneyHandler()
    return handler.handle(comando)
