# src/atribucion/modulos/atribucion/aplicacion/comandos/revertir_atribucion.py
from dataclasses import dataclass
from atribucion.seedwork.aplicacion.comandos import Comando, ejecutar_commando as comando, ComandoHandler

@dataclass
class RevertirAtribucion(Comando): 
    journey_id: str

class RevertirAtribucionHandler(ComandoHandler):
    def handle(self, comando: RevertirAtribucion):
        print("\n--- INICIO FLUJO REVERTIR ATRIBUCIÓN ---")
        print(f"HANDLER: Ejecutando RevertirAtribucionHandler")
        print(f"HANDLER: Se recibió la orden de revertir el Journey con ID: {comando.journey_id}")
        
        # PRÓXIMOS PASOS (los implementaremos después):
        # 1. Usar repositorio para buscar el Journey en la BD.
        # 2. Llamar a un método en la entidad Journey para cambiar el estado.
        # 3. Guardar los cambios con la Unidad de Trabajo.
        # 4. Publicar el evento de reversión con los IDs de los touchpoints.
        print("--- FIN FLUJO REVERTIR ATRIBUCIÓN ---\n")

@comando.register(RevertirAtribucion)
def ejecutar_comando_revertir_atribucion(comando: RevertirAtribucion):
    handler = RevertirAtribucionHandler()
    handler.handle(comando)