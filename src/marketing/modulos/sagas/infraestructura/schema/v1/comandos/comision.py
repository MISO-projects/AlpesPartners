from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion


class RevertirComisionPayload(Record):
    id_correlacion = String()
    journey_id = String()
    motivo = String()


class ComandoRevertirComision(ComandoIntegracion):
    data = RevertirComisionPayload()
