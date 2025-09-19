from marketing.seedwork.aplicacion.comandos import Comando
from dataclasses import dataclass
import uuid
from marketing.modulos.sagas.aplicacion.dto.atribucion import AtribucionDTO
from marketing.modulos.campanias.infraestructura.despachadores import DespachadorMarketing
from marketing.seedwork.aplicacion.comandos import ComandoHandler
from marketing.seedwork.aplicacion.comandos import ejecutar_commando as comando


@dataclass
class RegistrarAtribucion(Comando):
    atribucion: AtribucionDTO


@dataclass
class RevertirAtribucion(Comando):
    journey_id: uuid.UUID

class RevertirAtribucionHandler(ComandoHandler):
    def handle(self, comando: RevertirAtribucion):
        despachador = DespachadorMarketing()
        despachador.publicar_comando_revertir_atribucion(comando)

@comando.register(RevertirAtribucion)
def ejecutar_comando(comando: RevertirAtribucion):
    handler = RevertirAtribucionHandler()
    return handler.handle(comando)