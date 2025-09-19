import pulsar, _pulsar
from pulsar.schema import *
from tracking.modulos.interacciones.infraestructura.schema.v1.eventos import (
    EventoCampaniaActivada,
)
from tracking.modulos.interacciones.infraestructura.schema.v1.comandos import (
    ComandoDescartarInteracciones,
)
from tracking.seedwork.infraestructura import utils
import traceback
from tracking.seedwork.aplicacion.comandos import ejecutar_commando
from tracking.modulos.interacciones.aplicacion.comandos.descartar_interacciones import (
    DescartarInteracciones,
)


class ConsumidorEventosInteracciones:
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
                'campania-activada',
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='alpespartners-sub-eventos',
                schema=AvroSchema(EventoCampaniaActivada),
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            print(
                                f'Evento recibido en tracking: {mensaje.value().data}'
                            )
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f"Error procesando InteraccionRegistrada: {e}")
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)
        except Exception as e:
            print(f"Error configurando consumidor de atribución: {e}")
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()


class ConsumidorComandosInteracciones:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_comandos(self, app=None):
        if not app:
            return

        self.app = app

        try:
            self.cliente = pulsar.Client(
                f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            self.consumidor = self.cliente.subscribe(
                'descartar-interacciones-comando',
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='tracking-sub-comandos',
                schema=AvroSchema(ComandoDescartarInteracciones),
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_mensaje_con_comando(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f"Error procesando ComandoDescartarInteraccion: {e}")
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)
        except Exception as e:
            print(f"Error configurando consumidor de COMANDOS: {e}")
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_mensaje_con_comando(self, mensaje):

        payload = mensaje.value().data
        print(f'Comando recibido en tracking: {payload}')
        comando = DescartarInteracciones(interacciones=payload.interacciones)
        ejecutar_commando(comando)
