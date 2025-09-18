from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion


class DescartarInteraccionPayload(Record):
    id_interaccion = String()


class ComandoDescartarInteraccion(ComandoIntegracion):
    data = DescartarInteraccionPayload()
