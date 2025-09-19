from pulsar.schema import *
from comisiones.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

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

# Schemas para eventos que comisiones publica
class MontoComisionSchema(Record):
    valor = Float()
    moneda = String()

class ConfiguracionComisionSchema(Record):
    tipo = String()
    porcentaje = Float()

class ComisionReservadaPayload(Record):
    id_comision = String()
    id_interaccion = String()
    id_campania = String()
    monto = MontoComisionSchema()
    configuracion = ConfiguracionComisionSchema()
    timestamp = String()
    fraud_ok = Boolean()
    score_fraude = Integer()

class EventoComisionReservada(EventoIntegracion):
    data = ComisionReservadaPayload()

class ComisionCalculadaPayload(Record):
    id_comision = String()
    id_interaccion = String()
    id_campania = String()
    monto = MontoComisionSchema()
    tipo_calculo = String()
    timestamp = String()

class EventoComisionCalculada(EventoIntegracion):
    data = ComisionCalculadaPayload()

class RevertirComisionPayload(Record):
    journey_id = String()
    motivo = String()

class EventoRevertirComision(EventoIntegracion):
    data = RevertirComisionPayload()