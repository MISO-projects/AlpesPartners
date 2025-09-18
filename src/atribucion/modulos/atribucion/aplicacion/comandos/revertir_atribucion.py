# src/atribucion/modulos/atribucion/aplicacion/comandos/revertir_atribucion.py
from dataclasses import dataclass
from atribucion.seedwork.aplicacion.comandos import Comando, ejecutar_commando as comando, ComandoHandler
from atribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from atribucion.modulos.atribucion.infraestructura.despachadores import DespachadorEventosAtribucion
from atribucion.seedwork.dominio.excepciones import ExcepcionDominio

# --- Imports del Módulo ---
from atribucion.modulos.atribucion.dominio.entidades import Journey, EstadoJourney
from atribucion.modulos.atribucion.dominio.repositorios import RepositorioJourney
from .base import RevertirAtribucionBaseHandler # Asumimos que base.py existe

@dataclass
class RevertirAtribucion(Comando): 
    journey_id: str

class RevertirAtribucionHandler(RevertirAtribucionBaseHandler):
    def handle(self, comando: RevertirAtribucion):
        print("\n--- INICIO FLUJO REVERTIR ATRIBUCIÓN ---")
        print(f"HANDLER: Ejecutando RevertirAtribucionHandler para Journey ID: {comando.journey_id}")
        
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioJourney.__class__)
        journey: Journey = repositorio.obtener_por_id(comando.journey_id)
        
        if not journey:
            raise Exception(f"HANDLER: Journey con ID {comando.journey_id} no encontrado.")
        
        if journey.estado != EstadoJourney.CONVERTIDO:
            raise ExcepcionDominio(f"HANDLER: No se puede revertir un Journey en estado '{journey.estado.value}'.")

        journey.revertir_por_fraude()
        UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, journey)
        UnidadTrabajoPuerto.commit()
        
        despachador = DespachadorEventosAtribucion()
        despachador.publicar_evento_atribucion_revertida(journey)
        
        print("HANDLER: Commit realizado. Journey revertido exitosamente.")
        print("--- FIN FLUJO REVERTIR ATRIBUCIÓN ---\n")

@comando.register(RevertirAtribucion)
def ejecutar_comando_revertir_atribucion(comando: RevertirAtribucion):
    handler = RevertirAtribucionHandler()
    handler.handle(comando)