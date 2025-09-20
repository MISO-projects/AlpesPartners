from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from comisiones.seedwork.dominio.eventos import EventoDominio
from comisiones.modulos.comisiones.dominio.objetos_valor import (
    MontoComision,
    ConfiguracionComision,
    PoliticaFraude
)
import uuid

@dataclass
class ComisionReservada(EventoDominio):
    id_correlacion: str = None
    id_comision: uuid.UUID = None
    id_journey: uuid.UUID = None
    id_campania: uuid.UUID = None
    monto: MontoComision = None
    configuracion: ConfiguracionComision = None
    timestamp: datetime = None
    politica_fraude: PoliticaFraude = None

@dataclass
class ComisionCalculada(EventoDominio):
    """Evento que se publica cuando se ha calculado una comisión exitosamente"""

    id_comision: uuid.UUID = None
    id_interaccion: uuid.UUID = None
    id_campania: uuid.UUID = None
    monto: MontoComision = None
    configuracion: ConfiguracionComision = None
    timestamp: datetime = None
    politica_fraude: PoliticaFraude = None
    tipo_calculo: str = None 

@dataclass
class ComisionConfirmada(EventoDominio):

    id_comision: uuid.UUID = None
    monto_confirmado: MontoComision = None
    lote_confirmacion: str = None
    fecha_confirmacion: datetime = None

@dataclass
class ComisionRevertida(EventoDominio):
    id_comision: uuid.UUID = None
    journey_id: uuid.UUID = None
    monto_revertido: MontoComision = None
    motivo: str = None
    fecha_reversion: datetime = None

@dataclass
class ComisionCancelada(EventoDominio):

    id_comision: uuid.UUID = None
    motivo: str = None
    fecha_cancelacion: datetime = None

@dataclass
class PoliticaFraudeAplicada(EventoDominio):

    id_comision: uuid.UUID = None
    id_interaccion: uuid.UUID = None
    score_fraude: int = None
    politica_aplicada: PoliticaFraude = None
    resultado: str = None

@dataclass
class LoteComisionesConfirmadas(EventoDominio):

    id_lote: str = None
    comisiones_confirmadas: list[uuid.UUID] = None
    monto_total: MontoComision = None
    fecha_confirmacion: datetime = None
    cantidad_comisiones: int = None

@dataclass
class InteraccionAtribuidaRecibida(EventoDominio):

    id_interaccion: uuid.UUID = None
    id_campania: uuid.UUID = None
    tipo_interaccion: str = None
    valor_interaccion: MontoComision = None
    fraud_ok: bool = None
    score_fraude: int = None
    timestamp: datetime = None

@dataclass
class ConversionAtribuida(EventoDominio):
    """Evento que viene del AttributionService cuando hay una conversión atribuida"""
    
    id_interaccion: uuid.UUID = None
    id_campania: uuid.UUID = None
    tipo_interaccion: str = None
    valor_interaccion: MontoComision = None
    fraud_ok: bool = None
    score_fraude: int = None
    atribucion_data: dict = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.atribucion_data is None:
            self.atribucion_data = {}
