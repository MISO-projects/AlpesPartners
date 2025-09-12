
from comisiones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from comisiones.modulos.comisiones.aplicacion.comandos.reservar_comision import ReservarComision
from comisiones.modulos.comisiones.dominio.eventos import InteraccionAtribuidaRecibida
from comisiones.modulos.comisiones.dominio.objetos_valor import MontoComision
from comisiones.seedwork.aplicacion.comandos import ejecutar_commando
from decimal import Decimal
import uuid

class ConsumidorInteraccionAtribuida:

    def __init__(self):
        pass  

    def consumir_interaccion_atribuida(self, evento_tracking: dict):

        try:
            if not self._validar_evento_tracking(evento_tracking):
                print(f"Evento de tracking inválido: {evento_tracking}")
                return

            id_interaccion = uuid.UUID(evento_tracking.get('id_interaccion'))
            id_campania = evento_tracking.get('id_campania')
            tipo_interaccion = evento_tracking.get('tipo', 'UNKNOWN')
            
            valor_interaccion = self._calcular_valor_interaccion(evento_tracking)
            
            fraud_ok, score_fraude = self._evaluar_fraude(evento_tracking)

            comando = ReservarComision(
                id_interaccion=id_interaccion,
                id_campania=uuid.UUID(id_campania) if id_campania else uuid.uuid4(),
                tipo_interaccion=tipo_interaccion,
                valor_interaccion=valor_interaccion,
                moneda_interaccion="USD",
                fraud_ok=fraud_ok,
                score_fraude=score_fraude,
                parametros_adicionales=evento_tracking.get('parametros_tracking', {})
            )

            resultado = ejecutar_commando(comando)

            if resultado:
                print(f"Comisión {resultado.id} reservada exitosamente para interacción {id_interaccion}")
                
                evento_interaccion_atribuida = InteraccionAtribuidaRecibida(
                    id_interaccion=id_interaccion,
                    id_campania=uuid.UUID(id_campania) if id_campania else uuid.uuid4(),
                    tipo_interaccion=tipo_interaccion,
                    valor_interaccion=MontoComision(valor=valor_interaccion, moneda="USD"),
                    fraud_ok=fraud_ok,
                    score_fraude=score_fraude,
                    timestamp=evento_tracking.get('marca_temporal')
                )
                
                UnidadTrabajoPuerto.publicar_evento(evento_interaccion_atribuida)
            else:
                print(f"No se generó comisión para la interacción {id_interaccion}")

        except Exception as e:
            print(f"Error procesando evento de tracking: {e}")

    def _validar_evento_tracking(self, evento: dict) -> bool:

        campos_requeridos = ['id_interaccion', 'tipo']
        
        for campo in campos_requeridos:
            if campo not in evento:
                return False
        
        try:
            uuid.UUID(evento['id_interaccion'])
        except (ValueError, TypeError):
            return False
        
        return True

    def _calcular_valor_interaccion(self, evento_tracking: dict) -> Decimal:

        tipo_interaccion = evento_tracking.get('tipo', 'UNKNOWN')
        parametros = evento_tracking.get('parametros_tracking', {})
        
        valores_base = {
            'CLICK': Decimal('10.0'),
            'VIEW': Decimal('1.0'),
            'PURCHASE': Decimal('100.0'),
            'LEAD': Decimal('50.0'),
            'SIGNUP': Decimal('25.0'),
            'DOWNLOAD': Decimal('5.0'),
        }
        
        valor_base = valores_base.get(tipo_interaccion, Decimal('10.0'))
        
        if parametros.get('premium_user'):
            valor_base = valor_base * Decimal('1.5')
        
        if parametros.get('mobile_traffic'):
            valor_base = valor_base * Decimal('1.2')
        
        valor_especifico = parametros.get('valor_monetario')
        if valor_especifico:
            try:
                return Decimal(str(valor_especifico))
            except:
                pass
        
        return valor_base

    def _evaluar_fraude(self, evento_tracking: dict) -> tuple[bool, int]:

        parametros = evento_tracking.get('parametros_tracking', {})
        contexto = evento_tracking.get('contexto', {})
        
        score_fraude = 0
        
        if contexto.get('ip_sospechosa'):
            score_fraude += 30
        
        if contexto.get('user_agent_bot'):
            score_fraude += 40
        
        velocidad_clicks = parametros.get('clicks_per_minute', 0)
        if velocidad_clicks > 10:
            score_fraude += 25
        
        if contexto.get('geo_inconsistente'):
            score_fraude += 20
        
        score_fraude = min(score_fraude, 100)
        
        threshold = 50
        fraud_ok = score_fraude <= threshold
        
        return fraud_ok, score_fraude

class ConsumidorEventosComision:

    def consumir_comision_reservada(self, evento: dict):

        print(f"Procesando ComisionReservada: {evento.get('id_comision')}")

    def consumir_comision_confirmada(self, evento: dict):

        print(f"Procesando ComisionConfirmada: {evento.get('id_comision')}")

    def consumir_lote_confirmado(self, evento: dict):

        print(f"Procesando lote confirmado: {evento.get('id_lote')} - {evento.get('cantidad_comisiones')} comisiones")

