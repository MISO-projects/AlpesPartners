from marketing.seedwork.aplicacion.comandos import Comando
from dataclasses import dataclass
import uuid
from marketing.modulos.sagas.aplicacion.dto.atribucion import AtribucionDTO
from marketing.modulos.sagas.infraestructura.despachadores import DespachadorSagas
from marketing.seedwork.aplicacion.comandos import ComandoHandler
from marketing.seedwork.aplicacion.comandos import ejecutar_commando as comando


@dataclass
class RegistrarAtribucion(Comando):
    atribucion: AtribucionDTO


@dataclass
class RevertirAtribucion(Comando):
    id_correlacion: str
    journey_id: uuid.UUID

class RevertirAtribucionHandler(ComandoHandler):
    def handle(self, comando: RevertirAtribucion):
        despachador = DespachadorSagas()
        despachador.publicar_comando_revertir_atribucion(comando)

@comando.register(RevertirAtribucion)
def ejecutar_comando(comando: RevertirAtribucion):
    handler = RevertirAtribucionHandler()
    return handler.handle(comando)