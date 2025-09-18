import pulsar
from pulsar.schema import *
from marketing.modulos.sagas.infraestructura.schema.v1.eventos.tracking import (
    EventoInteraccionRegistradaConsumoSaga,
    EventoInteraccionDescartadaConsumoSaga,
)
from marketing.modulos.sagas.infraestructura.schema.v1.eventos.atribucion import (
    EventoConversionAtribuidaConsumoSaga,
    EventoAtribucionRevertidaConsumoSaga,
)
from marketing.modulos.sagas.infraestructura.schema.v1.eventos.comision import (
    EventoComisionReservadaConsumoSaga,
    EventoComisionRevertidaConsumoSaga,
)
from marketing.modulos.sagas.infraestructura.schema.v1.eventos.comision import (
    EventoFraudeDetectadoConsumoSaga,
)
from marketing.seedwork.infraestructura import utils
import traceback
from marketing.modulos.sagas.aplicacion.coordinadores.saga_interacciones import (
    procesar_evento_saga,
)
from marketing.modulos.sagas.dominio.eventos.tracking import (
    InteraccionRegistrada,
    InteraccionDescartada,
)
from marketing.modulos.sagas.dominio.eventos.atribucion import (
    ConversionAtribuida,
    AtribucionRevertida,
)
from marketing.modulos.sagas.dominio.eventos.comisiones import (
    ComisionReservada,
    ComisionRevertida,
    FraudeDetectado,
)
from marketing.seedwork.infraestructura.consumidores import BaseConsumidor


def avro_to_dict(record: Record) -> dict:
    if not isinstance(record, Record):
        return record

    result = {}
    for key, value in record.__dict__.items():
        if key.startswith('_'):
            continue
        if isinstance(value, Record):
            result[key] = avro_to_dict(value)
        elif isinstance(value, list):
            result[key] = [avro_to_dict(item) for item in value]
        else:
            result[key] = value
    return result


class ConsumidorInteracciones(BaseConsumidor):
    def get_subscription_config(self):
        return {
            'topico': 'interaccion-registrada',
            'subscription_name': 'marketing-sub-interacciones-saga',
            'schema_class': EventoInteraccionRegistradaConsumoSaga,
        }

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'📥 InteraccionRegistrada recibida en saga: {evento_dict}')
        event_dominio = InteraccionRegistrada(**evento_dict)
        procesar_evento_saga(event_dominio)


class ConsumidorInteraccionDescartada(BaseConsumidor):
    def get_subscription_config(self):
        return {
            'topico': 'interaccion-descartada',
            'subscription_name': 'marketing-sub-interaccion-descartada-saga',
            'schema_class': EventoInteraccionDescartadaConsumoSaga,
        }

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'📥 InteraccionDescartada recibida en saga: {evento_dict}')
        event_dominio = InteraccionDescartada(**evento_dict)
        procesar_evento_saga(event_dominio)


class ConsumidorAtribucion(BaseConsumidor):
    def get_subscription_config(self):
        return {
            'topico': 'eventos-atribucion',
            'subscription_name': 'marketing-sub-atribucion-saga',
            'schema_class': EventoConversionAtribuidaConsumoSaga,
        }

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'📥 ConversionAtribuida recibida en saga: {evento_dict}')
        event_dominio = ConversionAtribuida(**evento_dict)
        procesar_evento_saga(event_dominio)


class ConsumidorAtribucionRevertida(BaseConsumidor):
    def get_subscription_config(self):
        return {
            'topico': 'atribucion-revertida',
            'subscription_name': 'marketing-sub-atribucion-revertida-saga',
            'schema_class': EventoAtribucionRevertidaConsumoSaga,
        }

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'📥 AtribucionRevertida recibida en saga: {evento_dict}')
        event_dominio = AtribucionRevertida(**evento_dict)
        procesar_evento_saga(event_dominio)


class ConsumidorComisiones(BaseConsumidor):
    def get_subscription_config(self):
        return {
            'topico': 'comision-reservada',
            'subscription_name': 'marketing-sub-comision-reservada-saga',
            'schema_class': EventoComisionReservadaConsumoSaga,
        }

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'📥 ComisionReservada recibida en saga: {evento_dict}')
        event_dominio = ComisionReservada(**evento_dict)
        procesar_evento_saga(event_dominio)


class ConsumidorComisionesRevertidas(BaseConsumidor):
    def get_subscription_config(self):
        return {
            'topico': 'comision-revertida',
            'subscription_name': 'marketing-sub-comision-revertida-saga',
            'schema_class': EventoComisionRevertidaConsumoSaga,
        }

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'📥 ComisionRevertida recibida en saga: {evento_dict}')
        event_dominio = ComisionRevertida(**evento_dict)
        procesar_evento_saga(event_dominio)


class ConsumidorFraude(BaseConsumidor):
    def get_subscription_config(self):
        return {
            'topico': 'fraude-detectado',
            'subscription_name': 'marketing-sub-fraude-detectado-saga',
            'schema_class': EventoFraudeDetectadoConsumoSaga,
        }

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'📥 FraudeDetectado recibido en saga: {evento_dict}')
        event_dominio = FraudeDetectado(**evento_dict)
        procesar_evento_saga(event_dominio)
