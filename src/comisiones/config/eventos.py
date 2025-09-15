
import os
import pulsar
import json
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EventManager:

    def __init__(self):
        self.pulsar_url = os.getenv("PULSAR_URL", "pulsar://localhost:6650")
        self.client = None
        self.producer = None
        self.consumers = {}
        self.service_name = "comisiones"

    def connect(self):

        try:
            self.client = pulsar.Client(self.pulsar_url)
            
            self.producer = self.client.create_producer(
                topic=f"persistent://public/default/{self.service_name}-events",
                producer_name=f"{self.service_name}-producer"
            )
            
            logger.info(f"Conectado a Pulsar: {self.pulsar_url}")
            return True
            
        except Exception as e:
            logger.error(f"Error conectando a Pulsar: {e}")
            return False

    def disconnect(self):

        try:
            for consumer in self.consumers.values():
                consumer.close()
            
            if self.producer:
                self.producer.close()
            
            if self.client:
                self.client.close()
            
            logger.info("Desconectado de Pulsar")
            
        except Exception as e:
            logger.error(f"Error desconectando de Pulsar: {e}")

    def publish_event(self, event_type: str, event_data: Dict[str, Any]):

        try:
            event_message = {
                "event_id": f"{event_type}-{datetime.now().timestamp()}",
                "event_type": event_type,
                "service": self.service_name,
                "timestamp": datetime.now().isoformat(),
                "data": event_data
            }

            self.producer.send(
                content=json.dumps(event_message, default=str).encode('utf-8'),
                properties={
                    'event_type': event_type,
                    'service': self.service_name,
                    'version': '1.0'
                }
            )

            logger.info(f"Evento publicado: {event_type}")
            return True

        except Exception as e:
            logger.error(f"Error publicando evento {event_type}: {e}")
            return False

    def create_consumer(self, topic: str, subscription_name: str, message_handler):

        try:
            consumer = self.client.subscribe(
                topic=topic,
                subscription_name=subscription_name,
                consumer_type=pulsar.ConsumerType.Shared,
                message_listener=message_handler
            )
            
            self.consumers[topic] = consumer
            logger.info(f"Consumer creado para topic: {topic}")
            return consumer
            
        except Exception as e:
            logger.error(f"Error creando consumer para {topic}: {e}")
            return None

    def subscribe_to_tracking_events(self, handler):

        topic = "persistent://public/default/tracking-events"
        return self.create_consumer(topic, "comisiones-tracking-sub", handler)

    def subscribe_to_marketing_events(self, handler):

        topic = "persistent://public/default/marketing-events"
        return self.create_consumer(topic, "comisiones-marketing-sub", handler)

    def subscribe_to_attribution_events(self, handler):
        """Suscribirse a eventos del servicio de atribución"""
        topic = "persistent://public/default/attribution-events"
        return self.create_consumer(topic, "comisiones-attribution-sub", handler)

event_manager = EventManager()

def get_event_manager():

    return event_manager
