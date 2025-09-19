from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


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


class EventoConversionAtribuidaConsumoSaga(EventoIntegracion):
    data = ConversionAtribuidaPayload()


class AtribucionRevertidaPayload(Record):
    journey_id_revertido = String()
    interacciones = Array(String()) 

class EventoAtribucionRevertidaConsumoSaga(EventoIntegracion):
    data = AtribucionRevertidaPayload()