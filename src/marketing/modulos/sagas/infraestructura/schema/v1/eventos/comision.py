from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

# Schema para consumir eventos de atribución
class MontoSchema(Record):
    valor = Float()
    moneda = String()

class ConversionAtribuidaPayload(Record):
    id_correlacion = String()
    id_interaccion_atribuida = String()
    id_campania = String()
    id_afiliado = String()
    tipo_conversion = String()
    monto_atribuido = MontoSchema()
    id_interaccion_original = String()
    score_fraude = Integer()

class EventoConversionAtribuida(EventoIntegracion):
    data = ConversionAtribuidaPayload()

# Schemas para eventos que comisiones publica
class MontoComisionSchema(Record):
    valor = Float()
    moneda = String()

class ConfiguracionComisionSchema(Record):
    tipo = String()
    porcentaje = Float()

class ComisionReservadaPayload(Record):
    id_correlacion = String()
    id_comision = String()
    id_interaccion = String()
    id_campania = String()
    monto = MontoComisionSchema()
    configuracion = ConfiguracionComisionSchema()
    timestamp = String()
    fraud_ok = Boolean()
    score_fraude = Integer()

class EventoComisionReservadaConsumoSaga(EventoIntegracion):
    data = ComisionReservadaPayload()

class FraudeDetectadoPayload(Record):
    journey_id = String()

class EventoFraudeDetectadoConsumoSaga(EventoIntegracion):
    data = FraudeDetectadoPayload()

class ComisionRevertidaPayload(Record):
    id_comision = String()
    journey_id = String()
    monto_revertido = MontoComisionSchema()
    motivo = String()
    fecha_reversion = String()

class EventoComisionRevertidaConsumoSaga(EventoIntegracion):
    data = ComisionRevertidaPayload()