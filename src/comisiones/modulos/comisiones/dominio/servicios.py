
from typing import List
from datetime import datetime, timedelta
from alpespartners.modulos.comisiones.dominio.entidades import Comision
from alpespartners.modulos.comisiones.dominio.objetos_valor import (
    InteraccionAtribuida,
    ConfiguracionComision,
    PoliticaFraude,
    EstadoComision,
    MontoComision,
    TipoPoliticaFraude
)
from alpespartners.modulos.comisiones.dominio.repositorios import (
    RepositorioComision,
    RepositorioConfiguracionComision,
    RepositorioPoliticaFraude
)
from alpespartners.modulos.comisiones.dominio.excepciones import (
    InteraccionNoValidaParaComisionExcepcion,
    LoteComisionesInvalidoExcepcion
)
from alpespartners.seedwork.dominio.servicios import ServicioDominio
from decimal import Decimal
import uuid

class ServicioComision(ServicioDominio):

    def __init__(
        self,
        repositorio_comision: RepositorioComision,
        repositorio_configuracion: RepositorioConfiguracionComision,
        repositorio_politica_fraude: RepositorioPoliticaFraude
    ):
        self._repositorio_comision = repositorio_comision
        self._repositorio_configuracion = repositorio_configuracion
        self._repositorio_politica_fraude = repositorio_politica_fraude

    def procesar_interaccion_atribuida(self, interaccion: InteraccionAtribuida) -> Comision:
        if not self._es_interaccion_valida(interaccion):
            raise InteraccionNoValidaParaComisionExcepcion(
                f"La interacción {interaccion.id_interaccion} no es válida para generar comisión"
            )
        configuracion = self._obtener_configuracion_comision(interaccion)
        if not configuracion:
            return None
        politica_fraude = self._obtener_politica_fraude(interaccion)
        comision = Comision()
        comision.reservar_comision(interaccion, configuracion, politica_fraude)
        
        return comision

    def confirmar_comisiones_en_lote(
        self,
        limite_comisiones: int = 100,
        lote_id: str = None
    ) -> tuple[List[Comision], str]:

        if limite_comisiones <= 0:
            raise LoteComisionesInvalidoExcepcion("El límite debe ser mayor a 0")
        comisiones_reservadas = self._repositorio_comision.obtener_para_lote(limite_comisiones)
        
        if not comisiones_reservadas:
            return [], ""
        lote_confirmacion = lote_id or f"LOTE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        comisiones_confirmadas = []
        for comision in comisiones_reservadas:
            try:
                comision.confirmar_comision(lote_confirmacion=lote_confirmacion)
                comisiones_confirmadas.append(comision)
            except Exception as e:
                print(f"Error confirmando comisión {comision.id}: {e}")
        
        return comisiones_confirmadas, lote_confirmacion

    def limpiar_comisiones_vencidas(self, dias_vencimiento: int = 7) -> List[Comision]:

        fecha_limite = datetime.now() - timedelta(days=dias_vencimiento)
        comisiones_vencidas = self._repositorio_comision.obtener_reservadas_vencidas(fecha_limite)
        
        comisiones_canceladas = []
        for comision in comisiones_vencidas:
            try:
                comision.cancelar_comision(motivo="Comisión vencida por inactividad")
                comisiones_canceladas.append(comision)
            except Exception as e:
                print(f"Error cancelando comisión vencida {comision.id}: {e}")
        
        return comisiones_canceladas

    def calcular_comisiones_totales_campania(self, id_campania: uuid.UUID) -> dict:

        comisiones = self._repositorio_comision.obtener_por_campania(id_campania)
        
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
            estadisticas[comision.estado.value.lower()] += 1
            
            if comision.estado == EstadoComision.RESERVADA:
                estadisticas["monto_total_reservado"] += comision.monto.valor
            elif comision.estado == EstadoComision.CONFIRMADA:
                estadisticas["monto_total_confirmado"] += comision.monto.valor
            elif comision.estado == EstadoComision.REVERTIDA:
                estadisticas["monto_total_revertido"] += comision.monto.valor
        
        return estadisticas

    def _es_interaccion_valida(self, interaccion: InteraccionAtribuida) -> bool:
        if not interaccion.id_interaccion or not interaccion.id_campania:
            return False
        
        if not interaccion.fraud_ok:
            return False
        
        if not interaccion.valor_interaccion or interaccion.valor_interaccion.valor <= 0:
            return False
        try:
            comision_existente = self._repositorio_comision.obtener_por_interaccion(interaccion.id_interaccion)
            if comision_existente:
                return False
        except:
            pass
        
        return True

    def _obtener_configuracion_comision(self, interaccion: InteraccionAtribuida) -> ConfiguracionComision:
        try:
            configuracion = self._repositorio_configuracion.obtener_por_campania(interaccion.id_campania)
            if configuracion:
                return configuracion
        except:
            pass
        try:
            configuracion = self._repositorio_configuracion.obtener_por_tipo_interaccion(interaccion.tipo_interaccion)
            if configuracion:
                return configuracion
        except:
            pass
        return self._repositorio_configuracion.obtener_default()

    def _obtener_politica_fraude(self, interaccion: InteraccionAtribuida) -> PoliticaFraude:
        try:
            politica = self._repositorio_politica_fraude.obtener_por_campania(interaccion.id_campania)
            if politica:
                return politica
        except:
            pass
        return self._repositorio_politica_fraude.obtener_default()
