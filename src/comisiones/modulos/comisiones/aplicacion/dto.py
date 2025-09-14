
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, List
import uuid

@dataclass
class MontoComisionDTO:
    valor: Decimal
    moneda: str = "USD"

@dataclass
class ConfiguracionComisionDTO:
    tipo: str
    porcentaje: Optional[Decimal] = None
    monto_fijo: Optional[MontoComisionDTO] = None
    escalones: List[dict] = field(default_factory=list)
    minimo: Optional[MontoComisionDTO] = None
    maximo: Optional[MontoComisionDTO] = None

@dataclass
class PoliticaFraudeDTO:
    tipo: str
    threshold_score: int = 50
    requiere_revision_manual: bool = False
    tiempo_espera_minutos: int = 0

@dataclass
class InteraccionAtribuidaDTO:
    id_interaccion: uuid.UUID
    id_campania: uuid.UUID
    tipo_interaccion: str
    valor_interaccion: MontoComisionDTO
    fraud_ok: bool
    score_fraude: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    parametros_adicionales: Dict = field(default_factory=dict)

@dataclass
class ComisionDTO:
    id: uuid.UUID
    id_interaccion: str
    id_campania: str
    monto: MontoComisionDTO
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    configuracion: Optional[ConfiguracionComisionDTO] = None
    fecha_vencimiento: Optional[datetime] = None
    politica_fraude_aplicada: Optional[PoliticaFraudeDTO] = None

@dataclass
class DetallesReservaDTO:
    id_comision: uuid.UUID
    monto_reservado: MontoComisionDTO
    fecha_reserva: datetime
    referencia_interaccion: uuid.UUID
    motivo: str = ""
    metadata: Dict = field(default_factory=dict)

@dataclass
class DetallesConfirmacionDTO:
    fecha_confirmacion: datetime
    monto_confirmado: MontoComisionDTO
    lote_confirmacion: str = ""
    referencia_pago: str = ""
    metadata: Dict = field(default_factory=dict)

@dataclass
class EstadisticasComisionDTO:
    total_comisiones: int
    reservadas: int
    confirmadas: int
    revertidas: int
    canceladas: int
    monto_total_reservado: Decimal
    monto_total_confirmado: Decimal
    monto_total_revertido: Decimal

@dataclass
class LoteConfirmacionDTO:
    id_lote: str
    comisiones_confirmadas: List[uuid.UUID]
    monto_total: MontoComisionDTO
    fecha_confirmacion: datetime
    cantidad_comisiones: int
