from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion


class DescartarInteraccionPayload(Record):
    interacciones = Array(String())


class ComandoDescartarInteraccion(ComandoIntegracion):
    data = DescartarInteraccionPayload()
