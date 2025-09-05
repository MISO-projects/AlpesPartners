import pulsar
from pulsar.schema import AvroSchema
from alpespartners.modulos.tracking.infraestructura.schema.v1.eventos import (
    EventoInteraccionRegistrada
)
from alpespartners.modulos.marketing.aplicacion.handlers import (
    HandlerInteraccionTrackingRecibida
)
from alpespartners.seedwork.infraestructura import utils
import threading


class ConsumidorEventosTracking:
    def __init__(self):
        self.cliente = None
        self.consumidor = None
        self.ejecutando = False
        
    def _obtener_cliente(self):
        if not self.cliente:
            self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        return self.cliente
    
    def iniciar_consumo(self):
        cliente = self._obtener_cliente()
        
        try:
            self.consumidor = cliente.subscribe(
                topic="interaccion-registrada",
                subscription_name="marketing-service-subscription",
                schema=AvroSchema(EventoInteraccionRegistrada),
                consumer_type=pulsar.ConsumerType.Shared
            )
            
            self.ejecutando = True
            print(" Consumidor de Marketing iniciado - Escuchando eventos de Tracking...")
            
            while self.ejecutando:
                try:
                    mensaje = self.consumidor.receive(timeout_millis=5000)
                    
                    if mensaje:
                        evento_data = mensaje.value()
                        print(f" Evento recibido en Marketing: {evento_data}")
                        
                        handler = HandlerInteraccionTrackingRecibida()
                        handler.handle(evento_data)
                        
                        self.consumidor.acknowledge(mensaje)
                        print(" Evento procesado exitosamente en Marketing")
                        
                except pulsar.Timeout:
                    continue
                except Exception as e:
                    print(f" Error procesando evento en Marketing: {e}")
                    if mensaje:
                        self.consumidor.negative_acknowledge(mensaje)
                    
        except Exception as e:
            print(f" Error iniciando consumidor Marketing: {e}")
            raise e
        finally:
            if self.consumidor:
                self.consumidor.close()
            if cliente:
                cliente.close()

    def detener_consumo(self):
        self.ejecutando = False
        print(" Deteniendo consumidor de Marketing...")

    def iniciar_consumo_asincrono(self):
        hilo_consumidor = threading.Thread(target=self.iniciar_consumo)
        hilo_consumidor.daemon = True
        hilo_consumidor.start()
        print(" Consumidor Marketing iniciado de forma asíncrona")
        return hilo_consumidor


class ConsumidorComandosMarketing:

    def __init__(self):
        self.cliente = None
        self.ejecutando = False
        
    def _obtener_cliente(self):
        if not self.cliente:
            self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        return self.cliente

    def iniciar_consumo_comandos(self):
        cliente = self._obtener_cliente()
        
        try:
            consumidor_crear = cliente.subscribe(
                topic="crear-campania-comando",
                subscription_name="marketing-comandos-subscription",
                consumer_type=pulsar.ConsumerType.Shared
            )
            
            self.ejecutando = True
            print("Consumidor de Comandos Marketing iniciado...")
            
            while self.ejecutando:
                try:
                    mensaje = consumidor_crear.receive(timeout_millis=5000)
                    
                    if mensaje:
                        comando_data = mensaje.value()
                        print(f" Comando recibido en Marketing: {comando_data}")
                        

                        consumidor_crear.acknowledge(mensaje)
                        print(" Comando procesado exitosamente")
                        
                except pulsar.Timeout:
                    continue
                except Exception as e:
                    print(f" Error procesando comando: {e}")
                    if mensaje:
                        consumidor_crear.negative_acknowledge(mensaje)
                    
        except Exception as e:
            print(f" Error iniciando consumidor de comandos: {e}")
            raise e
        finally:
            if consumidor_crear:
                consumidor_crear.close()
            if cliente:
                cliente.close()
