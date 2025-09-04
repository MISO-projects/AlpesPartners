from pulsar.schema import *
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class ParametrosTrackingSchema(Record):
    fuente = String()
    medio = String()
    campania = String()
    contenido = String()
    termino = String()
    id_afiliado = String()


class IdentidadUsuarioSchema(Record):
    id_usuario = String(required=False)
    id_anonimo = String(required=False)
    direccion_ip = String(required=False)
    agente_usuario = String(required=False)


class ElementoObjetivoSchema(Record):
    url = String()
    id_elemento = String(required=False)


class ContextoInteraccionSchema(Record):
    url_pagina = String()
    url_referente = String(required=False)
    informacion_dispositivo = String(required=False)


class InteraccionRegistradaPayload(Record):
    id_interaccion = String()  # UUID as string
    tipo = String()
    marca_temporal = Long()  # Unix timestamp in milliseconds
    identidad_usuario = IdentidadUsuarioSchema()
    parametros_tracking = ParametrosTrackingSchema()
    elemento_objetivo = ElementoObjetivoSchema()
    contexto = ContextoInteraccionSchema()


class EventoInteraccionRegistrada(EventoIntegracion):
    data = InteraccionRegistradaPayload()
