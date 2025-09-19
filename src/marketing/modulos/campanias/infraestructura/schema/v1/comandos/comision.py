from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion


class RevertirComisionPayload(Record):
    journey_id = String()


class ComandoRevertirComision(ComandoIntegracion):
    data = RevertirComisionPayload()
