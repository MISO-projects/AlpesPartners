from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from comisiones.seedwork.dominio.entidades import AgregacionRaiz
from comisiones.modulos.comisiones.dominio.objetos_valor import (
    EstadoComision,
    MontoComision,
    ConfiguracionComision,
    InteraccionAtribuida,
    DetallesReserva,
    DetallesConfirmacion,
    PoliticaFraude
)
from comisiones.modulos.comisiones.dominio.eventos import (
    ComisionReservada,
    ComisionConfirmada,
    ComisionRevertida,
    ComisionCancelada,
    PoliticaFraudeAplicada
)
from comisiones.modulos.comisiones.dominio.excepciones import (
    ComisionYaConfirmadaExcepcion,
    ComisionYaRevertidaExcepcion,
    EstadoComisionInvalidoExcepcion,
    MontoComisionInvalidoExcepcion
)

@dataclass
class Comision(AgregacionRaiz):
    id_interaccion: str = field(default="")
    id_campania: str = field(default="")
    id_journey: str = field(default=None)
    monto: MontoComision = field(default=None)
    estado: EstadoComision = field(default=EstadoComision.RESERVADA)
    configuracion: ConfiguracionComision = field(default=None)
    detalles_reserva: DetallesReserva = field(default=None)
    detalles_confirmacion: DetallesConfirmacion = field(default=None)
    fecha_vencimiento: datetime = field(default=None)
    politica_fraude_aplicada: PoliticaFraude = field(default=None)
    
    def reservar_comision(
        self,
        interaccion: InteraccionAtribuida,
        configuracion: ConfiguracionComision,
        politica_fraude: PoliticaFraude
    ):

        if self.estado != EstadoComision.RESERVADA:
            raise EstadoComisionInvalidoExcepcion("Solo se pueden reservar comisiones en estado inicial")

        monto_calculado = self._calcular_monto_comision(interaccion.valor_interaccion, configuracion)
        
        self.id_interaccion = str(interaccion.id_interaccion)
        self.id_campania = str(interaccion.id_campania)
        self.monto = monto_calculado
        self.configuracion = configuracion
        self.politica_fraude_aplicada = politica_fraude
        
        self.detalles_reserva = DetallesReserva(
            id_comision=self.id,
            monto_reservado=monto_calculado,
            fecha_reserva=datetime.now(),
            referencia_interaccion=interaccion.id_interaccion,
            motivo="Comisión reservada por interacción atribuida",
            metadata={
                "tipo_interaccion": interaccion.tipo_interaccion,
                "score_fraude": interaccion.score_fraude,
                "fraud_ok": interaccion.fraud_ok
            }
        )
        
        self.agregar_evento(
            ComisionReservada(
                id_comision=self.id,
                id_interaccion=interaccion.id_interaccion,
                id_campania=interaccion.id_campania,
                monto=monto_calculado,
                configuracion=configuracion,
                timestamp=datetime.now(),
                politica_fraude=politica_fraude
            )
        )
    
    def confirmar_comision(self, lote_confirmacion: str = "", referencia_pago: str = ""):

        if self.estado != EstadoComision.RESERVADA:
            raise ComisionYaConfirmadaExcepcion("Solo se pueden confirmar comisiones reservadas")
        
        self.estado = EstadoComision.CONFIRMADA
        self.detalles_confirmacion = DetallesConfirmacion(
            fecha_confirmacion=datetime.now(),
            monto_confirmado=self.monto,
            lote_confirmacion=lote_confirmacion,
            referencia_pago=referencia_pago,
            metadata={"confirmado_automaticamente": True}
        )
        
        self.agregar_evento(
            ComisionConfirmada(
                id_comision=self.id,
                monto_confirmado=self.monto,
                lote_confirmacion=lote_confirmacion,
                fecha_confirmacion=datetime.now()
            )
        )
    
    def revertir_comision(self, motivo: str = ""):

        if self.estado == EstadoComision.REVERTIDA:
            raise ComisionYaRevertidaExcepcion("La comisión ya está revertida")
        
        if self.estado not in [EstadoComision.RESERVADA, EstadoComision.CONFIRMADA]:
            raise EstadoComisionInvalidoExcepcion("Solo se pueden revertir comisiones reservadas o confirmadas")
        
        self.estado = EstadoComision.REVERTIDA
        
        self.agregar_evento(
            ComisionRevertida(
                id_comision=self.id,
                journey_id=self.id_journey,
                monto_revertido=self.monto,
                motivo=motivo,
                fecha_reversion=datetime.now()
            )
        )
    
    def cancelar_comision(self, motivo: str = ""):

        if self.estado != EstadoComision.RESERVADA:
            raise EstadoComisionInvalidoExcepcion("Solo se pueden cancelar comisiones reservadas")
        
        self.estado = EstadoComision.CANCELADA
        
        self.agregar_evento(
            ComisionCancelada(
                id_comision=self.id,
                motivo=motivo,
                fecha_cancelacion=datetime.now()
            )
        )
    
    def _validar_politica_fraude(self, interaccion: InteraccionAtribuida, politica: PoliticaFraude) -> bool:

        if not interaccion.fraud_ok:
            return False
        
        if interaccion.score_fraude > politica.threshold_score:
            return False
        
        return True
    
    def _calcular_monto_comision(self, valor_interaccion: MontoComision, configuracion: ConfiguracionComision) -> MontoComision:

        from decimal import Decimal
        
        if configuracion.tipo.name == "PORCENTAJE":
            monto_calculado = valor_interaccion.valor * (configuracion.porcentaje / Decimal('100'))
        elif configuracion.tipo.name == "FIJO":
            monto_calculado = configuracion.monto_fijo.valor
        else:

            monto_calculado = valor_interaccion.valor * (Decimal('5') / Decimal('100'))
        if configuracion.minimo and monto_calculado < configuracion.minimo.valor:
            monto_calculado = configuracion.minimo.valor
        
        if configuracion.maximo and monto_calculado > configuracion.maximo.valor:
            monto_calculado = configuracion.maximo.valor
        
        return MontoComision(valor=monto_calculado, moneda=valor_interaccion.moneda)
