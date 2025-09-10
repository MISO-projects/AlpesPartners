from marketing.seedwork.aplicacion.comandos import Comando, ComandoHandler
from marketing.modulos.campanias.dominio.repositorios import RepositorioCampania
from marketing.modulos.campanias.infraestructura.fabricas import FabricaRepositorio
from marketing.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from marketing.seedwork.aplicacion.comandos import ejecutar_commando as comando
from dataclasses import dataclass
import uuid


@dataclass
class ActivarCampania(Comando):
    id_campania: str


class ActivarCampaniaHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        
    def handle(self, comando: ActivarCampania):
        try:
            repositorio = self._fabrica_repositorio.crear_objeto(RepositorioCampania.__class__)
            campania = repositorio.obtener_por_id(uuid.UUID(comando.id_campania))
            
            if not campania:
                raise Exception(f"Campaña con ID {comando.id_campania} no encontrada")
            
            campania.activar_campania()
            
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, campania)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()
            
            print(f" Campaña '{campania.nombre}' activada exitosamente")
            return campania
            
        except Exception as e:
            UnidadTrabajoPuerto.rollback()
            print(f" Error activando campaña: {e}")
            raise e

@comando.register(ActivarCampania)
def ejecutar_comando(comando: ActivarCampania):
    handler = ActivarCampaniaHandler()
    handler.handle(comando)