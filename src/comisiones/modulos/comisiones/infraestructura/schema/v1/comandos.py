from pulsar.schema import *
from comisiones.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class RevertirComisionPayload(Record):
    journey_id = String()
    motivo = String()


class ComandoRevertirComision(ComandoIntegracion):
    data = RevertirComisionPayload()
