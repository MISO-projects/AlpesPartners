
from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from datetime import datetime

from modulos.comisiones.dominio.entidades import Comision
from modulos.comisiones.dominio.objetos_valor import (
    InteraccionAtribuida,
    MontoComision,
    EstadoComision
)
from modulos.comisiones.dominio.servicios import ServicioComision
from modulos.comisiones.infraestructura.fabricas import FabricaRepositorio
from modulos.comisiones.dominio.repositorios import (
    RepositorioComision,
    RepositorioConfiguracionComision,
    RepositorioPoliticaFraude
)
from config.eventos import EventManager
import logging

logger = logging.getLogger(__name__)

class ComisionService:
    
    def __init__(self, db_session: Session, event_manager: EventManager):
        self.db_session = db_session
        self.event_manager = event_manager
        self._fabrica_repositorio = FabricaRepositorio()
        
    def _get_servicio_dominio(self) -> ServicioComision:
        repositorio_comision = self._fabrica_repositorio.crear_objeto(
            RepositorioComision.__class__
        )
        repositorio_configuracion = self._fabrica_repositorio.crear_objeto(
            RepositorioConfiguracionComision.__class__
        )
        repositorio_politica_fraude = self._fabrica_repositorio.crear_objeto(
            RepositorioPoliticaFraude.__class__
        )
        
        return ServicioComision(
            repositorio_comision=repositorio_comision,
            repositorio_configuracion=repositorio_configuracion,
            repositorio_politica_fraude=repositorio_politica_fraude
        )
    
    async def reservar_comision(
        self,
        id_interaccion: UUID,
        id_campania: UUID,
        tipo_interaccion: str,
        valor_interaccion: Decimal,
        moneda_interaccion: str = "USD",
        fraud_ok: bool = True,
        score_fraude: int = 0,
        parametros_adicionales: Dict[str, Any] = None
    ) -> Optional[Comision]:
        try:
            interaccion = InteraccionAtribuida(
                id_interaccion=id_interaccion,
                id_campania=id_campania,
                tipo_interaccion=tipo_interaccion,
                valor_interaccion=MontoComision(
                    valor=valor_interaccion,
                    moneda=moneda_interaccion
                ),
                fraud_ok=fraud_ok,
                score_fraude=score_fraude,
                parametros_adicionales=parametros_adicionales or {}
            )
            
            servicio_dominio = self._get_servicio_dominio()
            comision = servicio_dominio.procesar_interaccion_atribuida(interaccion)
            
            if comision:
                repositorio = self._fabrica_repositorio.crear_objeto(
                    RepositorioComision.__class__
                )
                repositorio.agregar(comision)
                self.db_session.commit()
                
                await self._publicar_evento_comision_calculada(comision, interaccion)
                
                logger.info(f"Comisión {comision.id} reservada exitosamente")
                return comision
            
            return None
            
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error reservando comisión: {e}")
            raise e
    
    async def confirmar_comision(
        self,
        id_comision: UUID,
        lote_confirmacion: str = "",
        referencia_pago: str = ""
    ) -> Comision:
        try:
            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )
            
            comision = repositorio.obtener_por_id(id_comision)
            if not comision:
                raise ValueError(f"Comisión {id_comision} no encontrada")
            
            comision.confirmar_comision(lote_confirmacion, referencia_pago)
            repositorio.actualizar(comision)
            self.db_session.commit()
            
            await self._publicar_evento_comision_confirmada(comision)
            
            logger.info(f"Comisión {comision.id} confirmada exitosamente")
            return comision
            
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error confirmando comisión: {e}")
            raise e
    
    async def confirmar_comisiones_en_lote(
        self,
        limite_comisiones: int = 100,
        lote_id: str = None
    ) -> Dict[str, Any]:
        try:
            servicio_dominio = self._get_servicio_dominio()
            comisiones_confirmadas, lote_confirmacion = servicio_dominio.confirmar_comisiones_en_lote(
                limite_comisiones=limite_comisiones,
                lote_id=lote_id
            )
            
            if comisiones_confirmadas:
                repositorio = self._fabrica_repositorio.crear_objeto(
                    RepositorioComision.__class__
                )
                for comision in comisiones_confirmadas:
                    repositorio.actualizar(comision)
                
                self.db_session.commit()
                
 de lote
                await self._publicar_evento_lote_confirmado(comisiones_confirmadas, lote_confirmacion)
                
                logger.info(f"Lote {lote_confirmacion}: {len(comisiones_confirmadas)} comisiones confirmadas")
            
            return {
                "lote_id": lote_confirmacion,
                "cantidad_confirmadas": len(comisiones_confirmadas),
                "comisiones": comisiones_confirmadas
            }
            
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error confirmando lote: {e}")
            raise e
    
    async def revertir_comision(
        self,
        id_comision: UUID,
        motivo: str
    ) -> Comision:
        try:
            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )
            
            comision = repositorio.obtener_por_id(id_comision)
            if not comision:
                raise ValueError(f"Comisión {id_comision} no encontrada")
            
            comision.revertir_comision(motivo)
            repositorio.actualizar(comision)
            self.db_session.commit()
            
            await self._publicar_evento_comision_revertida(comision, motivo)
            
            logger.info(f"Comisión {comision.id} revertida exitosamente")
            return comision
            
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error revirtiendo comisión: {e}")
            raise e
    
    async def obtener_comision_por_id(self, id_comision: UUID) -> Optional[Comision]:
        try:
            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )
            return repositorio.obtener_por_id(id_comision)
            
        except Exception as e:
            logger.error(f"Error obteniendo comisión {id_comision}: {e}")
            return None
    
    async def listar_comisiones(
        self,
        estado: Optional[str] = None,
        id_campania: Optional[UUID] = None,
        para_lote: bool = False,
        limite: int = 100
    ) -> List[Comision]:
        try:
            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )
            
            if para_lote:
                return repositorio.obtener_para_lote(limite)
            elif estado:
                return repositorio.obtener_por_estado(EstadoComision(estado))
            elif id_campania:
                return repositorio.obtener_por_campania(id_campania)
            else:
                return repositorio.obtener_todos()
                
        except Exception as e:
            logger.error(f"Error listando comisiones: {e}")
            return []
    
    async def obtener_estadisticas_comisiones(
        self,
        id_campania: Optional[UUID] = None
    ) -> Dict[str, Any]:
        try:
            if id_campania:
                servicio_dominio = self._get_servicio_dominio()
                return servicio_dominio.calcular_comisiones_totales_campania(id_campania)
            else:
                repositorio = self._fabrica_repositorio.crear_objeto(
                    RepositorioComision.__class__
                )
                todas_comisiones = repositorio.obtener_todos()
                
                return self._calcular_estadisticas_generales(todas_comisiones)
                
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def _calcular_estadisticas_generales(self, comisiones: List[Comision]) -> Dict[str, Any]:
        from decimal import Decimal
        
        estadisticas = {
            "total_comisiones": len(comisiones),
            "reservadas": 0,
            "confirmadas": 0,
            "revertidas": 0,
            "canceladas": 0,
            "monto_total_reservado": Decimal('0'),
            "monto_total_confirmado": Decimal('0'),
            "monto_total_revertido": Decimal('0')
        }
        
        for comision in comisiones:
            if comision.estado == EstadoComision.RESERVADA:
                estadisticas["reservadas"] += 1
                estadisticas["monto_total_reservado"] += comision.monto.valor
            elif comision.estado == EstadoComision.CONFIRMADA:
                estadisticas["confirmadas"] += 1
                estadisticas["monto_total_confirmado"] += comision.monto.valor
            elif comision.estado == EstadoComision.REVERTIDA:
                estadisticas["revertidas"] += 1
                estadisticas["monto_total_revertido"] += comision.monto.valor
            elif comision.estado == EstadoComision.CANCELADA:
                estadisticas["canceladas"] += 1
        
        return estadisticas
    
    async def _publicar_evento_comision_calculada(self, comision: Comision, interaccion: InteraccionAtribuida):
        """Publicar evento comisionCalculada como indica el diagrama"""
        try:
            event_data = {
                "id_comision": str(comision.id),
                "id_interaccion": str(interaccion.id_interaccion),
                "id_campania": str(interaccion.id_campania),
                "monto_comision": {
                    "valor": float(comision.monto.valor),
                    "moneda": comision.monto.moneda
                },
                "estado": str(comision.estado),
                "tipo_interaccion": interaccion.tipo_interaccion,
                "score_fraude": interaccion.score_fraude,
                "configuracion_aplicada": self._serialize_configuracion(comision),
                "timestamp": datetime.now().isoformat()
            }
            
            self.event_manager.publish_event("comisionCalculada", event_data)
            logger.info(f"Evento comisionCalculada publicado para comisión {comision.id}")
            
        except Exception as e:
            logger.error(f"Error publicando evento comisionCalculada: {e}")
    
    def _serialize_configuracion(self, comision: Comision) -> Optional[Dict[str, Any]]:
        """Serializar configuración de comisión para el evento"""
        try:
            if hasattr(comision, 'configuracion') and comision.configuracion:
                return {
                    "tipo": str(comision.configuracion.tipo) if hasattr(comision.configuracion, 'tipo') else None,
                    "porcentaje": float(comision.configuracion.porcentaje) if hasattr(comision.configuracion, 'porcentaje') else None,
                    "monto_fijo": float(comision.configuracion.monto_fijo.valor) if hasattr(comision.configuracion, 'monto_fijo') and comision.configuracion.monto_fijo else None
                }
            return None
        except Exception as e:
            logger.warning(f"Error serializando configuración: {e}")
            return None
    
    async def _publicar_evento_comision_confirmada(self, comision: Comision):
        try:
            event_data = {
                "id_comision": str(comision.id),
                "monto": {
                    "valor": str(comision.monto.valor),
                    "moneda": comision.monto.moneda
                },
                "estado": comision.estado.value
            }
            
            self.event_manager.publish_event("ComisionConfirmada", event_data)
            
        except Exception as e:
            logger.error(f"Error publicando evento ComisionConfirmada: {e}")
    
    async def _publicar_evento_comision_revertida(self, comision: Comision, motivo: str):
        try:
            event_data = {
                "id_comision": str(comision.id),
                "monto": {
                    "valor": str(comision.monto.valor),
                    "moneda": comision.monto.moneda
                },
                "motivo": motivo
            }
            
            self.event_manager.publish_event("ComisionRevertida", event_data)
            
        except Exception as e:
            logger.error(f"Error publicando evento ComisionRevertida: {e}")
    
    async def _publicar_evento_lote_confirmado(self, comisiones: List[Comision], lote_id: str):
        try:
            from decimal import Decimal
            
            monto_total = sum(comision.monto.valor for comision in comisiones)
            
            event_data = {
                "lote_id": lote_id,
                "cantidad_comisiones": len(comisiones),
                "monto_total": {
                    "valor": str(monto_total),
                    "moneda": comisiones[0].monto.moneda if comisiones else "USD"
                },
                "comisiones": [str(comision.id) for comision in comisiones]
            }
            
            self.event_manager.publish_event("LoteComisionesConfirmadas", event_data)
            
        except Exception as e:
            logger.error(f"Error publicando evento LoteComisionesConfirmadas: {e}")
