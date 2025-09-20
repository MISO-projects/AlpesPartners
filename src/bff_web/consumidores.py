import logging
import traceback
import pulsar
import aiopulsar
import asyncio
import json
from . import utils

def suscribirse_a_eventos_campanias(eventos_campanias=[]):
    """
    Consumer que escucha eventos de campañas creadas desde el servicio de marketing
    y los agrega a la lista para Server-Sent Events
    """
    cliente = None
    try:
        print(f"🔄 BFF conectando a Pulsar: {utils.broker_host()}:6650")

        # Conectar a Pulsar usando client sync
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')

        # Suscribirse al tópico
        consumidor = cliente.subscribe(
            'campania-creada',  # Tópico donde marketing publica eventos
            consumer_type=pulsar.ConsumerType.Shared,
            subscription_name='bff-campanias-sub'
            # Sin schema para recibir JSON simple
        )

        print("✓ BFF suscrito a eventos de campañas")

        while True:
            try:
                # Recibir mensaje con timeout
                mensaje = consumidor.receive(timeout_millis=100)

                # Deserializar el evento
                datos_evento = json.loads(mensaje.value().decode('utf-8'))
                nombre_campania = datos_evento.get('data', {}).get('nombre', 'Sin nombre')
                print(f"📧 Campaña recibida: {nombre_campania}")

                # Agregar a la lista de eventos para SSE
                evento_sse = {
                    'tipo': 'campania_creada',
                    'datos': datos_evento,
                    'timestamp': utils.time_millis()
                }
                eventos_campanias.append(evento_sse)

                # Acknowledge el mensaje
                consumidor.acknowledge(mensaje)

            except Exception as e:
                if "Timeout" not in str(e) and "TimeOut" not in str(e):
                    print(f"❌ Error procesando evento: {e}")

    except Exception as e:
        print(f'❌ ERROR: BFF suscribiéndose a eventos de campañas: {e}')
        traceback.print_exc()
    finally:
        if cliente:
            cliente.close()