
import json
import logging
import asyncio
from typing import Dict, Any
import pulsar

from config.eventos import get_event_manager
from services.comision_service import ComisionService
from config.db import SessionLocal

logger = logging.getLogger(__name__)

class EventService:
    
    def __init__(self):
        self.event_manager = get_event_manager()
        self.consumers = []
        self.running = False
    
    async def start(self):
        logger.info("Iniciando servicio de eventos...")
        
        try:
            tracking_consumer = self.event_manager.subscribe_to_tracking_events(
                self._handle_tracking_event
            )
            
            if tracking_consumer:
                self.consumers.append(tracking_consumer)
                logger.info("Suscrito a eventos de tracking")
            
            marketing_consumer = self.event_manager.subscribe_to_marketing_events(
                self._handle_marketing_event
            )
            
            if marketing_consumer:
                self.consumers.append(marketing_consumer)
                logger.info("Suscrito a eventos de marketing")
            
            self.running = True
            logger.info("Servicio de eventos iniciado")
            
        except Exception as e:
            logger.error(f"Error iniciando servicio de eventos: {e}")
            raise e
    
    async def stop(self):
        logger.info("Deteniendo servicio de eventos...")
        
        self.running = False
        
        for consumer in self.consumers:
            try:
                consumer.close()
            except Exception as e:
                logger.error(f"Error cerrando consumer: {e}")
        
        self.consumers.clear()
        logger.info("Servicio de eventos detenido")
    
    def _handle_tracking_event(self, consumer, message):
        try:
            data = json.loads(message.data().decode('utf-8'))
            event_type = data.get('event_type', 'unknown')
            event_data = data.get('data', {})
            
            logger.info(f"Evento de tracking recibido: {event_type}")
            
            if event_type == "InteraccionRegistrada":
                asyncio.create_task(self._process_interaccion_registrada(event_data))
            else:
                logger.info(f"Evento de tracking ignorado: {event_type}")
            
            consumer.acknowledge(message)
            
        except Exception as e:
            logger.error(f"Error procesando evento de tracking: {e}")
            consumer.negative_acknowledge(message)
    
    def _handle_marketing_event(self, consumer, message):
        try:
            data = json.loads(message.data().decode('utf-8'))
            event_type = data.get('event_type', 'unknown')
            event_data = data.get('data', {})
            
            logger.info(f"Evento de marketing recibido: {event_type}")
            
            if event_type == "CampaniaActivada":
                asyncio.create_task(self._process_campania_activada(event_data))
            elif event_type == "CampaniaDesactivada":
                asyncio.create_task(self._process_campania_desactivada(event_data))
            else:
                logger.info(f"Evento de marketing ignorado: {event_type}")
            
            consumer.acknowledge(message)
            
        except Exception as e:
            logger.error(f"Error procesando evento de marketing: {e}")
            consumer.negative_acknowledge(message)
    
    async def _process_interaccion_registrada(self, event_data: Dict[str, Any]):
        try:
            logger.info(f"Procesando InteraccionRegistrada: {event_data.get('id_interaccion')}")
            
            id_interaccion = event_data.get('id_interaccion')
            tipo_interaccion = event_data.get('tipo', 'UNKNOWN')
            
            contexto = event_data.get('contexto', {})
            parametros = event_data.get('parametros_tracking', {})
            id_campania = parametros.get('id_campania') or contexto.get('id_campania')
            
            if not id_interaccion or not id_campania:
                logger.warning("InteraccionRegistrada sin id_interaccion o id_campania válidos")
                return
            
            valor_interaccion = self._calculate_interaction_value(tipo_interaccion, parametros)
            
            fraud_ok, score_fraude = self._evaluate_fraud(event_data)
            
            db_session = SessionLocal()
            try:
                comision_service = ComisionService(db_session, self.event_manager)
                
                comision = await comision_service.reservar_comision(
                    id_interaccion=id_interaccion,
                    id_campania=id_campania,
                    tipo_interaccion=tipo_interaccion,
                    valor_interaccion=valor_interaccion,
                    fraud_ok=fraud_ok,
                    score_fraude=score_fraude,
                    parametros_adicionales=parametros
                )
                
                if comision:
                    logger.info(f"Comisión {comision.id} creada para interacción {id_interaccion}")
                else:
                    logger.info(f"No se generó comisión para interacción {id_interaccion}")
                    
            finally:
                db_session.close()
                
        except Exception as e:
            logger.error(f"Error procesando InteraccionRegistrada: {e}")
    
    async def _process_campania_activada(self, event_data: Dict[str, Any]):
        try:
            id_campania = event_data.get('id_campania')
            nombre_campania = event_data.get('nombre', 'Unknown')
            
            logger.info(f"Campaña activada: {nombre_campania} ({id_campania})")

        except Exception as e:
            logger.error(f"Error procesando CampaniaActivada: {e}")
    
    async def _process_campania_desactivada(self, event_data: Dict[str, Any]):
        try:
            id_campania = event_data.get('id_campania')
            
            logger.info(f"Campaña desactivada: {id_campania}")

        except Exception as e:
            logger.error(f"Error procesando CampaniaDesactivada: {e}")
    
    def _calculate_interaction_value(self, tipo_interaccion: str, parametros: Dict[str, Any]) -> float:
        from decimal import Decimal
        
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
            valor_base *= Decimal('1.5')
        
        if parametros.get('mobile_traffic'):
            valor_base *= Decimal('1.2')
        
        valor_especifico = parametros.get('valor_monetario')
        if valor_especifico:
            try:
                return Decimal(str(valor_especifico))
            except:
                pass
        
        return valor_base
    
    def _evaluate_fraud(self, event_data: Dict[str, Any]) -> tuple[bool, int]:
        parametros = event_data.get('parametros_tracking', {})
        contexto = event_data.get('contexto', {})
        
        score_fraude = 0
        
        if contexto.get('ip_sospechosa'):
            score_fraude += 30
        
        if contexto.get('user_agent_bot'):
            score_fraude += 40
        
        if parametros.get('clicks_per_minute', 0) > 10:
            score_fraude += 25
        
        if contexto.get('geo_inconsistente'):
            score_fraude += 20
        
        score_fraude = min(score_fraude, 100)
        
        threshold = 50
        fraud_ok = score_fraude <= threshold
        
        return fraud_ok, score_fraude
