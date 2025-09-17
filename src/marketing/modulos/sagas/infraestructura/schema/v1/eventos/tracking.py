from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class IdentidadUsuarioSchema(Record):
    id_usuario = String()
    id_anonimo = String()
    direccion_ip = String()
    agente_usuario = String()


class ParametrosTrackingSchema(Record):
    fuente = String()
    medio = String()
    campania = String()
    contenido = String()
    termino = String()
    id_afiliado = String()


class ElementoObjetivoSchema(Record):
    url = String()
    id_elemento = String()


class ContextoInteraccionSchema(Record):
    url_pagina = String()
    url_referente = String()
    informacion_dispositivo = String()


class InteraccionRegistradaPayload(Record):
    id_interaccion = String()
    tipo = String()
    marca_temporal = Long()
    identidad_usuario = IdentidadUsuarioSchema()
    parametros_tracking = ParametrosTrackingSchema()
    elemento_objetivo = ElementoObjetivoSchema()
    contexto = ContextoInteraccionSchema()


class EventoInteraccionRegistradaConsumoSaga(EventoIntegracion):
    data = InteraccionRegistradaPayload()
