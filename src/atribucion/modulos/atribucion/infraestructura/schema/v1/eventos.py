from pulsar.schema import *
from atribucion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

# evento recibido en atribucion desde tracking
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

class EventoInteraccionRegistradaConsumo(EventoIntegracion):
    data = InteraccionRegistradaPayload()


# schema para consumir eventos de atribución a comisiones
class MontoSchema(Record):
    valor = Float()
    moneda = String()

class ConversionAtribuidaPayload(Record):
    id_interaccion_atribuida = String()
    id_campania = String()
    id_afiliado = String()
    tipo_conversion = String()
    monto_atribuido = MontoSchema()
    id_interaccion_original = String()
    score_fraude = Integer()
class EventoConversionAtribuida(EventoIntegracion):
    data = ConversionAtribuidaPayload()


# --- Schema del Evento de Reversión ---

class AtribucionRevertidaPayload(Record):
    journey_id_revertido = String()
    interacciones = Array(String()) 

class EventoAtribucionRevertida(EventoIntegracion):
    data = AtribucionRevertidaPayload()