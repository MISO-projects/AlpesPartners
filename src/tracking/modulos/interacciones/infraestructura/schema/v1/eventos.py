from pulsar.schema import *
from tracking.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


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
    estado = String()


class EventoInteraccionRegistrada(EventoIntegracion):
    data = InteraccionRegistradaPayload()


class SegmentoAudienciaSchema(Record):
    edad_minima = Integer(required=False)
    edad_maxima = Integer(required=False)
    genero = String(required=False)
    ubicacion = String(required=False)
    intereses = Array(String(), required=False)


class CampaniaCreadaPayload(Record):
    id_campania = String()
    nombre = String()
    tipo = String()
    fecha_inicio = Long()
    fecha_fin = Long()
    segmento = SegmentoAudienciaSchema()


class CampaniaActivadaPayload(Record):
    id_campania = String()
    nombre = String()
    fecha_activacion = Long()


class CampaniaDesactivadaPayload(Record):
    id_campania = String()
    razon = String()
    fecha_desactivacion = Long()


class InteraccionRecibidaPayload(Record):
    id_campania = String()
    tipo_interaccion = String()
    parametros_tracking = Map(String())
    timestamp = Long()  #


class EventoCampaniaCreada(EventoIntegracion):
    data = CampaniaCreadaPayload()


class EventoCampaniaActivada(EventoIntegracion):
    data = CampaniaActivadaPayload()


class EventoCampaniaDesactivada(EventoIntegracion):
    data = CampaniaDesactivadaPayload()


class EventoInteraccionRecibida(EventoIntegracion):
    data = InteraccionRecibidaPayload()
