import pulsar, _pulsar
from pulsar.schema import *
from tracking.modulos.interacciones.infraestructura.schema.v1.eventos import (
    EventoCampaniaActivada
)
from tracking.seedwork.infraestructura import utils
import traceback


def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(
            'campania-activada',
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='alpespartners-sub-eventos',
            schema=AvroSchema(EventoCampaniaActivada),
        )

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido en tracking: {datos}')
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        print('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos(app=None): ...
