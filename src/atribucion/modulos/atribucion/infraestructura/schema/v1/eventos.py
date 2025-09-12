from pulsar.schema import *
from atribucion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class MontoComisionSchema(Record):
    valor = Double()
    moneda = String()


class InteraccionAtribuidaRecibidaPayload(Record):
    id_interaccion = String()
    id_campania = String()
    tipo_interaccion = String()
    valor_interaccion = MontoComisionSchema()
    fraud_ok = Boolean()
    score_fraude = Integer()
    timestamp = Long()


class EventoInteraccionAtribuidaRecibida(EventoIntegracion):
    data = InteraccionAtribuidaRecibidaPayload()


class ParametrosTrackingSchema(Record):
    """Schema local para consumir parámetros de tracking"""
    fuente = String()
    medio = String()
    campania = String()
    contenido = String()
    termino = String()
    id_afiliado = String()


class IdentidadUsuarioSchema(Record):
    """Schema local para consumir identidad de usuario"""
    id_usuario = String(required=False)
    id_anonimo = String(required=False)
    direccion_ip = String(required=False)
    agente_usuario = String(required=False)


class ElementoObjetivoSchema(Record):
    """Schema local para consumir elemento objetivo"""
    url = String()
    id_elemento = String(required=False)


class ContextoInteraccionSchema(Record):
    """Schema local para consumir contexto de interacción"""
    url_pagina = String()
    url_referente = String(required=False)
    informacion_dispositivo = String(required=False)


class InteraccionRegistradaPayload(Record):
    """Schema local para consumir InteraccionRegistrada desde Tracking"""
    id_interaccion = String()
    tipo = String()
    marca_temporal = Long()
    identidad_usuario = IdentidadUsuarioSchema()
    parametros_tracking = ParametrosTrackingSchema()
    elemento_objetivo = ElementoObjetivoSchema()
    contexto = ContextoInteraccionSchema()


class EventoInteraccionRegistradaConsumo(EventoIntegracion):
    """Evento de integración para consumir InteraccionRegistrada"""
    data = InteraccionRegistradaPayload()