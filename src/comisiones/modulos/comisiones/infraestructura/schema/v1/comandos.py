from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
import uuid

class ReservarComisionRequest(BaseModel):

    id_interaccion: uuid.UUID = Field(..., description="ID único de la interacción")
    id_campania: uuid.UUID = Field(..., description="ID de la campaña")
    tipo_interaccion: str = Field(..., description="Tipo de interacción (CLICK, VIEW, PURCHASE, etc.)")
    valor_interaccion: Decimal = Field(..., gt=0, description="Valor monetario de la interacción")
    moneda_interaccion: str = Field(default="USD", description="Moneda de la interacción")
    fraud_ok: bool = Field(default=True, description="Indica si pasó validación de fraude")
    score_fraude: int = Field(default=0, ge=0, le=100, description="Puntaje de fraude (0-100)")
    parametros_adicionales: Optional[Dict[str, Any]] = Field(default=None, description="Parámetros adicionales")

    @validator('moneda_interaccion')
    def validar_moneda(cls, v):
        monedas_validas = ['USD', 'EUR', 'COP', 'MXN', 'ARS', 'BRL', 'CLP']
        if v not in monedas_validas:
            raise ValueError(f'Moneda debe ser una de: {", ".join(monedas_validas)}')
        return v

    @validator('tipo_interaccion')
    def validar_tipo_interaccion(cls, v):
        tipos_validos = ['CLICK', 'VIEW', 'PURCHASE', 'LEAD', 'SIGNUP', 'DOWNLOAD', 'SHARE']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de interacción debe ser uno de: {", ".join(tipos_validos)}')
        return v

    class Config:
        schema_extra = {
            "example": {
                "id_interaccion": "123e4567-e89b-12d3-a456-426614174000",
                "id_campania": "987fcdeb-51a2-43d1-b123-456789abcdef",
                "tipo_interaccion": "CLICK",
                "valor_interaccion": "25.50",
                "moneda_interaccion": "USD",
                "fraud_ok": True,
                "score_fraude": 15,
                "parametros_adicionales": {
                    "source": "facebook",
                    "campaign_name": "summer_promo"
                }
            }
        }

class ConfirmarComisionRequest(BaseModel):

    id_comision: uuid.UUID = Field(..., description="ID único de la comisión")
    lote_confirmacion: Optional[str] = Field(default="", description="ID del lote de confirmación")
    referencia_pago: Optional[str] = Field(default="", description="Referencia del pago")

    class Config:
        schema_extra = {
            "example": {
                "id_comision": "456e7890-e12b-34d5-c678-901234567890",
                "lote_confirmacion": "LOTE_20241201_143025_abc12345",
                "referencia_pago": "PAY_20241201_COMM_001"
            }
        }

class ConfirmarComisionesEnLoteRequest(BaseModel):

    limite_comisiones: int = Field(default=100, gt=0, le=1000, description="Límite de comisiones a procesar")
    lote_id: Optional[str] = Field(default=None, description="ID personalizado del lote")

    @validator('limite_comisiones')
    def validar_limite(cls, v):
        if v > 1000:
            raise ValueError('El límite máximo es 1000 comisiones por lote')
        return v

    class Config:
        schema_extra = {
            "example": {
                "limite_comisiones": 50,
                "lote_id": "LOTE_MANUAL_20241201"
            }
        }

class RevertirComisionRequest(BaseModel):

    id_comision: uuid.UUID = Field(..., description="ID único de la comisión")
    motivo: str = Field(..., min_length=1, max_length=500, description="Motivo de la reversión")

    class Config:
        schema_extra = {
            "example": {
                "id_comision": "456e7890-e12b-34d5-c678-901234567890",
                "motivo": "Transacción fraudulenta detectada después de la confirmación"
            }
        }

class CancelarComisionRequest(BaseModel):

    id_comision: uuid.UUID = Field(..., description="ID único de la comisión")
    motivo: str = Field(..., min_length=1, max_length=500, description="Motivo de la cancelación")

    class Config:
        schema_extra = {
            "example": {
                "id_comision": "456e7890-e12b-34d5-c678-901234567890",
                "motivo": "Interacción no válida detectada en revisión"
            }
        }

class ComisionResponse(BaseModel):

    id: uuid.UUID
    id_interaccion: str
    id_campania: str
    monto_valor: Decimal
    monto_moneda: str
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    fecha_vencimiento: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "456e7890-e12b-34d5-c678-901234567890",
                "id_interaccion": "123e4567-e89b-12d3-a456-426614174000",
                "id_campania": "987fcdeb-51a2-43d1-b123-456789abcdef",
                "monto_valor": "5.25",
                "monto_moneda": "USD",
                "estado": "RESERVADA",
                "fecha_creacion": "2024-12-01T14:30:25Z",
                "fecha_actualizacion": "2024-12-01T14:30:25Z",
                "fecha_vencimiento": None
            }
        }

class LoteConfirmacionResponse(BaseModel):

    lote_id: str
    cantidad_confirmadas: int
    monto_total: Decimal
    moneda: str
    fecha_confirmacion: datetime
    comisiones_confirmadas: list[uuid.UUID]

    class Config:
        schema_extra = {
            "example": {
                "lote_id": "LOTE_20241201_143025_abc12345",
                "cantidad_confirmadas": 25,
                "monto_total": "1250.75",
                "moneda": "USD",
                "fecha_confirmacion": "2024-12-01T14:35:10Z",
                "comisiones_confirmadas": [
                    "456e7890-e12b-34d5-c678-901234567890",
                    "789f1234-e56c-78d9-e012-345678901234"
                ]
            }
        }

class ComandoResponse(BaseModel):

    exitoso: bool
    mensaje: str
    data: Optional[Any] = None
    errores: Optional[list[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "exitoso": True,
                "mensaje": "Comisión reservada exitosamente",
                "data": {
                    "id_comision": "456e7890-e12b-34d5-c678-901234567890"
                },
                "errores": None
            }
        }
