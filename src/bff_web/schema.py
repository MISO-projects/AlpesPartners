from pulsar.schema import *
from .utils import time_millis
import uuid


class Mensaje(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()


class EventoIntegracion(Mensaje): ...


class FraudeDetectadoPayload(Record):
    id_correlacion = String()
    journey_id = String()


class EventoFraudeDetectadoIntegracion(EventoIntegracion):
    data = FraudeDetectadoPayload()

