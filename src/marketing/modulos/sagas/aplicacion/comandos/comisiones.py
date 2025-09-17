from marketing.seedwork.aplicacion.comandos import Comando, ComandoHandler
from dataclasses import dataclass
import uuid
from decimal import Decimal
from marketing.seedwork.aplicacion.comandos import ejecutar_commando as comando
from marketing.modulos.campanias.infraestructura.despachadores import (
    DespachadorMarketing,
)


@dataclass
class ReservarComision(Comando):

    id_interaccion: uuid.UUID
    id_campania: uuid.UUID
    tipo_interaccion: str
    valor_interaccion: Decimal
    moneda_interaccion: str = "USD"
    fraud_ok: bool = True
    score_fraude: int = 0
    parametros_adicionales: dict = None


@dataclass
class RevertirComision(Comando):
    id_interaccion: uuid.UUID


class RevertirComisionHandler(ComandoHandler):
    def handle(self, comando: RevertirComision):
        despachador = DespachadorMarketing()
        despachador.publicar_comando_revertir_comision(comando)


@comando.register(RevertirComision)
def ejecutar_comando(comando: RevertirComision):
    handler = RevertirComisionHandler()
    return handler.handle(comando)
