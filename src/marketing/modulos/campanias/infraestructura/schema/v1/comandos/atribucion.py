from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion


class RevertirAtribucionPayload(Record):
    id_interaccion = String()


class ComandoRevertirAtribucion(ComandoIntegracion):
    data = RevertirAtribucionPayload()
