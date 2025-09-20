from tracking.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion
from datetime import datetime
from pulsar.schema import *


class ComandoRegistrarInteraccionPayload(ComandoIntegracion):
    tipo: str
    marca_temporal: datetime
    identidad_usuario: str
    parametros_tracking: str
    elemento_objetivo: str
    contexto: str


class ComandoRegistrarInteraccion(ComandoIntegracion):
    data = ComandoRegistrarInteraccionPayload()

class DescartarInteraccionesPayload(Record):
    id_correlacion = String()
    interacciones = Array(String())


class ComandoDescartarInteracciones(ComandoIntegracion):
    data = DescartarInteraccionesPayload()
