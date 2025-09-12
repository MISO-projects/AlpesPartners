import pulsar
import _pulsar
from pulsar.schema import AvroSchema
from atribucion.modulos.atribucion.infraestructura.schema.v1.eventos import EventoInteraccionRegistradaConsumo
from atribucion.seedwork.infraestructura import utils
import traceback


class ConsumidorInteracciones:
    """Consumidor de eventos InteraccionRegistrada desde el servicio de Tracking"""

    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_eventos_interaccion(self, app=None):
        """Configura la suscripción al evento InteraccionRegistrada"""
        try:
            self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
            self.consumidor = self.cliente.subscribe(
                'interaccion-registrada',
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='atribucion-sub-interacciones',
                schema=AvroSchema(EventoInteraccionRegistradaConsumo)
            )
            print("Consumidor Atribucion: Esperando eventos InteraccionRegistrada...")

            while True:
                mensaje = self.consumidor.receive()
                try:
                    self._procesar_evento_interaccion_registrada(mensaje)
                    self.consumidor.acknowledge(mensaje)
                    print(f"Evento InteraccionRegistrada procesado exitosamente")
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

    def _procesar_evento_interaccion_registrada(self, mensaje):
        """Procesa el evento InteraccionRegistrada y ejecuta la lógica de atribución"""
        evento_data = mensaje.value().data
        print(f" Atribución procesando InteraccionRegistrada:")
        print(f" - ID: {evento_data.id_interaccion}")
        print(f" - Tipo: {evento_data.tipo}")
        print(f" - Usuario: {evento_data.identidad_usuario.id_usuario or 'Anónimo'}")
        print(f" - Campaña: {evento_data.parametros_tracking.campania}")
        print(f" - Timestamp: {evento_data.marca_temporal}")
        
        # Ejecutar lógica de atribución
        resultado_atribucion = self._ejecutar_logica_atribucion(evento_data)
        
        if resultado_atribucion:
            print(f" ✅ Atribución exitosa - Disparando evento InteraccionAtribuidaRecibida")
            self._disparar_evento_atribucion(evento_data, resultado_atribucion)
        else:
            print(f" ❌ Atribución fallida - No se disparará evento")
        
        return True
    
    def _ejecutar_logica_atribucion(self, evento_data):
        """Lógica simplificada de atribución - TODO: Implementar lógica completa"""
        print(f" 🔍 Ejecutando lógica de atribución...")
        
        # Por ahora, atribuimos si hay campaña en los parámetros
        campania = evento_data.parametros_tracking.campania
        if campania and campania.strip():
            return {
                'id_campania': 'c60e66b4-b12a-43b0-b97a-b5eaff030cae',
                'valor_interaccion': {'valor': 25.50, 'moneda': 'USD'},
                'fraud_ok': True,
                'score_fraude': 15
            }
        return None
    
    def _disparar_evento_atribucion(self, evento_original, resultado):
        """Dispara el evento InteraccionAtribuidaRecibida"""
        from datetime import datetime
        from decimal import Decimal
        from atribucion.modulos.atribucion.dominio.eventos import InteraccionAtribuidaRecibida
        from atribucion.modulos.atribucion.dominio.objetos_valor import MontoComision
        from pydispatch import dispatcher
        
        # Crear el evento de atribución
        evento_atribucion = InteraccionAtribuidaRecibida(
            id_interaccion=evento_original.id_interaccion or 'unknown',
            id_campania=resultado['id_campania'],
            tipo_interaccion=evento_original.tipo,
            valor_interaccion=MontoComision(
                valor=Decimal(str(resultado['valor_interaccion']['valor'])),
                moneda=resultado['valor_interaccion']['moneda']
            ),
            fraud_ok=resultado['fraud_ok'],
            score_fraude=resultado['score_fraude'],
            timestamp=datetime.now()
        )
        
        # Disparar evento de integración
        dispatcher.send(signal=f'{InteraccionAtribuidaRecibida.__name__}Integracion', evento=evento_atribucion)