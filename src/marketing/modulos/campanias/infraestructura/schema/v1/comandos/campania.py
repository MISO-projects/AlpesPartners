from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion
from datetime import datetime


class CrearCampaniaPayload(Record):
    nombre = String()
    descripcion = String()
    fecha_inicio = Long()
    fecha_fin = Long()
    tipo = String()
    segmento = Map(String())
    configuracion = Map(String())


class ActivarCampaniaPayload(Record):
    id_campania = String()
    fecha_activacion = Long()


class ComandoCrearCampania(ComandoIntegracion):
    data = CrearCampaniaPayload()


class ComandoActivarCampania(ComandoIntegracion):
    data = ActivarCampaniaPayload()
