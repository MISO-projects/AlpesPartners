# src/atribucion/modulos/atribucion/infraestructura/schema/v1/comandos.py
from pulsar.schema import *
from atribucion.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class RevertirAtribucionPayload(Record):
    journey_id = String()

class ComandoRevertirAtribucion(ComandoIntegracion):
    data = RevertirAtribucionPayload()