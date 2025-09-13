
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal
import uuid

class MontoSchema(BaseModel):

    valor: Decimal = Field(..., description="Valor del monto")
    moneda: str = Field(..., description="Código de moneda (ISO 4217)")

    class Config:
        schema_extra = {
            "example": {
                "valor": "25.50",
                "moneda": "USD"
            }
        }

class ConfiguracionComisionSchema(BaseModel):

    tipo: str = Field(..., description="Tipo de comisión (PORCENTAJE, FIJO, ESCALONADO)")
    porcentaje: Optional[Decimal] = Field(None, description="Porcentaje de comisión")
    monto_fijo: Optional[MontoSchema] = Field(None, description="Monto fijo de comisión")
    escalones: Optional[List[Dict[str, Any]]] = Field(None, description="Escalones para comisión escalonada")
    minimo: Optional[MontoSchema] = Field(None, description="Monto mínimo")
    maximo: Optional[MontoSchema] = Field(None, description="Monto máximo")

class PoliticaFraudeSchema(BaseModel):

    tipo: str = Field(..., description="Tipo de política (STRICT, MODERATE, PERMISSIVE)")
    threshold_score: int = Field(..., description="Puntaje umbral de fraude")
    requiere_revision_manual: bool = Field(..., description="Si requiere revisión manual")
    tiempo_espera_minutos: int = Field(..., description="Tiempo de espera en minutos")

class ComisionReservadaEventSchema(BaseModel):

    tipo_evento: str = Field(default="ComisionReservada", description="Tipo de evento")
    id_comision: uuid.UUID = Field(..., description="ID de la comisión")
    id_interaccion: uuid.UUID = Field(..., description="ID de la interacción")
    id_campania: uuid.UUID = Field(..., description="ID de la campaña")
    monto: MontoSchema = Field(..., description="Monto de la comisión")
    configuracion: ConfiguracionComisionSchema = Field(..., description="Configuración aplicada")
    timestamp: datetime = Field(..., description="Timestamp del evento")
    politica_fraude: PoliticaFraudeSchema = Field(..., description="Política de fraude aplicada")

    class Config:
        schema_extra = {
            "example": {
                "tipo_evento": "ComisionReservada",
                "id_comision": "456e7890-e12b-34d5-c678-901234567890",
                "id_interaccion": "123e4567-e89b-12d3-a456-426614174000",
                "id_campania": "987fcdeb-51a2-43d1-b123-456789abcdef",
                "monto": {
                    "valor": "5.25",
                    "moneda": "USD"
                },
                "configuracion": {
                    "tipo": "PORCENTAJE",
                    "porcentaje": "5.0"
                },
                "timestamp": "2024-12-01T14:30:25Z",
                "politica_fraude": {
                    "tipo": "MODERATE",
                    "threshold_score": 50,
                    "requiere_revision_manual": False,
                    "tiempo_espera_minutos": 0
                }
            }
        }

class ComisionConfirmadaEventSchema(BaseModel):

    tipo_evento: str = Field(default="ComisionConfirmada", description="Tipo de evento")
    id_comision: uuid.UUID = Field(..., description="ID de la comisión")
    monto_confirmado: MontoSchema = Field(..., description="Monto confirmado")
    lote_confirmacion: str = Field(..., description="ID del lote de confirmación")
    fecha_confirmacion: datetime = Field(..., description="Fecha de confirmación")

    class Config:
        schema_extra = {
            "example": {
                "tipo_evento": "ComisionConfirmada",
                "id_comision": "456e7890-e12b-34d5-c678-901234567890",
                "monto_confirmado": {
                    "valor": "5.25",
                    "moneda": "USD"
                },
                "lote_confirmacion": "LOTE_20241201_143025_abc12345",
                "fecha_confirmacion": "2024-12-01T14:35:10Z"
            }
        }

class ComisionRevertidaEventSchema(BaseModel):

    tipo_evento: str = Field(default="ComisionRevertida", description="Tipo de evento")
    id_comision: uuid.UUID = Field(..., description="ID de la comisión")
    monto_revertido: MontoSchema = Field(..., description="Monto revertido")
    motivo: str = Field(..., description="Motivo de la reversión")
    fecha_reversion: datetime = Field(..., description="Fecha de reversión")

    class Config:
        schema_extra = {
            "example": {
                "tipo_evento": "ComisionRevertida",
                "id_comision": "456e7890-e12b-34d5-c678-901234567890",
                "monto_revertido": {
                    "valor": "5.25",
                    "moneda": "USD"
                },
                "motivo": "Transacción fraudulenta detectada",
                "fecha_reversion": "2024-12-01T16:45:30Z"
            }
        }

class ComisionCanceladaEventSchema(BaseModel):

    tipo_evento: str = Field(default="ComisionCancelada", description="Tipo de evento")
    id_comision: uuid.UUID = Field(..., description="ID de la comisión")
    motivo: str = Field(..., description="Motivo de la cancelación")
    fecha_cancelacion: datetime = Field(..., description="Fecha de cancelación")

    class Config:
        schema_extra = {
            "example": {
                "tipo_evento": "ComisionCancelada",
                "id_comision": "456e7890-e12b-34d5-c678-901234567890",
                "motivo": "Interacción no válida",
                "fecha_cancelacion": "2024-12-01T15:20:15Z"
            }
        }

class LoteComisionesConfirmadasEventSchema(BaseModel):

    tipo_evento: str = Field(default="LoteComisionesConfirmadas", description="Tipo de evento")
    id_lote: str = Field(..., description="ID del lote")
    comisiones_confirmadas: List[uuid.UUID] = Field(..., description="Lista de IDs de comisiones confirmadas")
    monto_total: MontoSchema = Field(..., description="Monto total del lote")
    fecha_confirmacion: datetime = Field(..., description="Fecha de confirmación del lote")
    cantidad_comisiones: int = Field(..., description="Cantidad de comisiones en el lote")

    class Config:
        schema_extra = {
            "example": {
                "tipo_evento": "LoteComisionesConfirmadas",
                "id_lote": "LOTE_20241201_143025_abc12345",
                "comisiones_confirmadas": [
                    "456e7890-e12b-34d5-c678-901234567890",
                    "789f1234-e56c-78d9-e012-345678901234"
                ],
                "monto_total": {
                    "valor": "1250.75",
                    "moneda": "USD"
                },
                "fecha_confirmacion": "2024-12-01T14:35:10Z",
                "cantidad_comisiones": 25
            }
        }

class PoliticaFraudeAplicadaEventSchema(BaseModel):

    tipo_evento: str = Field(default="PoliticaFraudeAplicada", description="Tipo de evento")
    id_comision: uuid.UUID = Field(..., description="ID de la comisión")
    id_interaccion: uuid.UUID = Field(..., description="ID de la interacción")
    score_fraude: int = Field(..., description="Puntaje de fraude")
    politica_aplicada: PoliticaFraudeSchema = Field(..., description="Política aplicada")
    resultado: str = Field(..., description="Resultado de la aplicación (APROBADA/RECHAZADA)")

    class Config:
        schema_extra = {
            "example": {
                "tipo_evento": "PoliticaFraudeAplicada",
                "id_comision": "456e7890-e12b-34d5-c678-901234567890",
                "id_interaccion": "123e4567-e89b-12d3-a456-426614174000",
                "score_fraude": 75,
                "politica_aplicada": {
                    "tipo": "STRICT",
                    "threshold_score": 30,
                    "requiere_revision_manual": True,
                    "tiempo_espera_minutos": 60
                },
                "resultado": "RECHAZADA"
            }
        }

class InteraccionAtribuidaRecibidaEventSchema(BaseModel):

    tipo_evento: str = Field(default="InteraccionAtribuidaRecibida", description="Tipo de evento")
    id_interaccion: uuid.UUID = Field(..., description="ID de la interacción")
    id_campania: uuid.UUID = Field(..., description="ID de la campaña")
    tipo_interaccion: str = Field(..., description="Tipo de interacción")
    valor_interaccion: MontoSchema = Field(..., description="Valor de la interacción")
    fraud_ok: bool = Field(..., description="Si pasó validación de fraude")
    score_fraude: int = Field(..., description="Puntaje de fraude")
    timestamp: datetime = Field(..., description="Timestamp del evento")

    class Config:
        schema_extra = {
            "example": {
                "tipo_evento": "InteraccionAtribuidaRecibida",
                "id_interaccion": "123e4567-e89b-12d3-a456-426614174000",
                "id_campania": "987fcdeb-51a2-43d1-b123-456789abcdef",
                "tipo_interaccion": "CLICK",
                "valor_interaccion": {
                    "valor": "25.50",
                    "moneda": "USD"
                },
                "fraud_ok": True,
                "score_fraude": 15,
                "timestamp": "2024-12-01T14:30:25Z"
            }
        }

class EventoComisionSchema(BaseModel):

    evento_id: uuid.UUID = Field(..., description="ID único del evento")
    timestamp: datetime = Field(..., description="Timestamp del evento")
    servicio: str = Field(default="comisiones", description="Servicio que emite el evento")
    version: str = Field(default="v1", description="Versión del esquema")
    datos: Dict[str, Any] = Field(..., description="Datos específicos del evento")

    class Config:
        schema_extra = {
            "example": {
                "evento_id": "987f6543-e21d-45a8-b123-456789abcdef",
                "timestamp": "2024-12-01T14:30:25Z",
                "servicio": "comisiones",
                "version": "v1",
                "datos": {
                    "tipo_evento": "ComisionReservada",
                    "id_comision": "456e7890-e12b-34d5-c678-901234567890"
                }
            }
        }
