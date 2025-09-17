import pulsar
from pulsar.schema import *
from marketing.modulos.sagas.infraestructura.schema.v1.eventos.tracking import (
    EventoInteraccionRegistradaConsumoSaga,
)
from marketing.modulos.sagas.infraestructura.schema.v1.eventos.atribucion import (
    EventoConversionAtribuidaConsumoSaga,
)
from marketing.modulos.sagas.infraestructura.schema.v1.eventos.comision import (
    EventoComisionReservadaConsumoSaga,
)
from marketing.modulos.sagas.infraestructura.schema.v1.eventos.comision import (
    EventoFraudeDetectadoConsumoSaga,
)
from marketing.seedwork.infraestructura import utils
import traceback
from marketing.modulos.sagas.aplicacion.coordinadores.saga_interacciones import (
    procesar_evento_saga,
)
from marketing.modulos.sagas.dominio.eventos.tracking import InteraccionRegistrada
from marketing.modulos.sagas.dominio.eventos.atribucion import ConversionAtribuida
from marketing.modulos.sagas.dominio.eventos.comisiones import (
    ComisionReservada,
    FraudeDetectado,
)


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


class ConsumidorInteracciones:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_eventos(self, app=None):
        if not app:
            return

        self.app = app
        try:
            self.cliente = pulsar.Client(
                f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            self.consumidor = self.cliente.subscribe(
                'interaccion-registrada',
                consumer_type=pulsar.ConsumerType.Shared,
                subscription_name='marketing-sub-interacciones-saga',
                schema=AvroSchema(EventoInteraccionRegistradaConsumoSaga),
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_evento_saga(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f'Error procesando evento: {e}')
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)

        except Exception as e:
            print(f'Error suscribiendose a eventos: {e}')
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'Evento recibido en saga marketing: {evento_dict}')
        event_dominio = InteraccionRegistrada(**evento_dict)
        procesar_evento_saga(event_dominio)


class ConsumidorAtribucion:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_eventos(self, app=None):
        if not app:
            return

        self.app = app
        try:
            self.cliente = pulsar.Client(
                f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            self.consumidor = self.cliente.subscribe(
                'eventos-atribucion',
                consumer_type=pulsar.ConsumerType.Shared,
                subscription_name='marketing-sub-atribucion-saga',
                schema=AvroSchema(EventoConversionAtribuidaConsumoSaga),
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_evento_saga(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f'Error procesando evento: {e}')
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)

        except Exception as e:
            print(f'Error suscribiendose a eventos: {e}')
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'Evento recibido en saga marketing: {evento_dict}')
        event_dominio = ConversionAtribuida(**evento_dict)
        procesar_evento_saga(event_dominio)


class ConsumidorComisiones:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_eventos(self, app=None):
        if not app:
            return

        self.app = app
        try:
            self.cliente = pulsar.Client(
                f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            self.consumidor = self.cliente.subscribe(
                'comision-reservada',
                consumer_type=pulsar.ConsumerType.Shared,
                subscription_name='marketing-sub-comision-reservada-saga',
                schema=AvroSchema(EventoComisionReservadaConsumoSaga),
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_evento_saga(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f'Error procesando evento: {e}')
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)

        except Exception as e:
            print(f'Error suscribiendose a eventos: {e}')
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'Evento recibido en saga marketing: {evento_dict}')
        event_dominio = ComisionReservada(**evento_dict)
        procesar_evento_saga(event_dominio)


class ConsumidorFraude:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_eventos(self, app=None):
        if not app:
            return

        self.app = app
        try:
            self.cliente = pulsar.Client(
                f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            self.consumidor = self.cliente.subscribe(
                'fraude-detectado',
                consumer_type=pulsar.ConsumerType.Shared,
                subscription_name='marketing-sub-fraude-detectado-saga',
                schema=AvroSchema(EventoFraudeDetectadoConsumoSaga),
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_evento_saga(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f'Error procesando evento: {e}')
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)

        except Exception as e:
            print(f'Error suscribiendose a eventos: {e}')
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_evento_saga(self, mensaje):
        evento_dict = avro_to_dict(mensaje.value().data)
        print(f'Evento recibido en saga marketing: {evento_dict}')
        event_dominio = FraudeDetectado(**evento_dict)
        procesar_evento_saga(event_dominio)
