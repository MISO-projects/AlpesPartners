from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion


class DescartarInteraccionesPayload(Record):
    interacciones = Array(String())


class ComandoDescartarInteracciones(ComandoIntegracion):
    data = DescartarInteraccionesPayload()
