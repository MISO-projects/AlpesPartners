from pulsar.schema import *
from marketing.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


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
