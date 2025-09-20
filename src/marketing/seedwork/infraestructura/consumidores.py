import pulsar
from pulsar.schema import *
from marketing.seedwork.infraestructura import utils
import traceback
from abc import ABC, abstractmethod


class BaseConsumidor(ABC):
    """Base class for all Pulsar consumers with common functionality"""

    def __init__(self):
        self.cliente = None
        self.consumidor = None
        self.app = None

    def _crear_cliente(self):
        """Create a Pulsar client with error-only logging"""
        return pulsar.Client(
            f'pulsar://{utils.broker_host()}:6650',
            logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
        )

    def _suscribirse_a_topico(self, topico, subscription_name, schema_class):
        """Generic method to subscribe to any topic"""
        try:
            self.cliente = self._crear_cliente()
            self.consumidor = self.cliente.subscribe(
                topico,
                consumer_type=pulsar.ConsumerType.Shared,
                subscription_name=subscription_name,
                schema=AvroSchema(schema_class),
            )
            return True
        except Exception as e:
            print(f'❌ Error suscribiendose a {topico}: {e}')
            traceback.print_exc()
            return False

    def _procesar_mensajes(self, procesador_callback):
        """Generic message processing loop"""
        try:
            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            procesador_callback(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f'❌ Error procesando evento: {e}')
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)
        finally:
            if self.cliente:
                self.cliente.close()

    def suscribirse_a_eventos(self, app=None):
        """Main subscription method - to be implemented by subclasses"""
        if not app:
            return

        self.app = app

        # Get subscription config from subclass
        config = self.get_subscription_config()

        if self._suscribirse_a_topico(
            config['topico'], config['subscription_name'], config['schema_class']
        ):
            self._procesar_mensajes(self._procesar_evento_saga)

    @abstractmethod
    def get_subscription_config(self):
        """Return subscription configuration"""
        pass

    @abstractmethod
    def _procesar_evento_saga(self, mensaje):
        """Process the received message"""
        pass
