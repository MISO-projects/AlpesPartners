
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from config.db import get_db
from config.eventos import get_event_manager
from services.comision_service import ComisionService

router = APIRouter()
class ReservarComisionRequest(BaseModel):
    id_interaccion: UUID = Field(..., description="ID único de la interacción")
    id_campania: UUID = Field(..., description="ID de la campaña")
    tipo_interaccion: str = Field(..., description="Tipo de interacción")
    valor_interaccion: Decimal = Field(..., gt=0, description="Valor monetario de la interacción")
    moneda_interaccion: str = Field(default="USD", description="Moneda de la interacción")
    fraud_ok: bool = Field(default=True, description="Si pasó validación de fraude")
    score_fraude: int = Field(default=0, ge=0, le=100, description="Puntaje de fraude")
    parametros_adicionales: Optional[dict] = Field(default=None, description="Parámetros adicionales")

class ConfirmarComisionRequest(BaseModel):
    lote_confirmacion: Optional[str] = Field(default="", description="ID del lote")
    referencia_pago: Optional[str] = Field(default="", description="Referencia de pago")

class ConfirmarLoteRequest(BaseModel):
    limite_comisiones: int = Field(default=100, gt=0, le=1000, description="Límite de comisiones")
    lote_id: Optional[str] = Field(default=None, description="ID personalizado del lote")

class RevertirComisionRequest(BaseModel):
    motivo: str = Field(..., min_length=1, max_length=500, description="Motivo de la reversión")

class ComisionResponse(BaseModel):
    id: UUID
    id_interaccion: str
    id_campania: str
    monto_valor: Decimal
    monto_moneda: str
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    fecha_vencimiento: Optional[datetime] = None

class ApiResponse(BaseModel):
    exitoso: bool
    mensaje: str
    data: Optional[dict] = None
    errores: Optional[List[str]] = None

def get_comision_service(db: Session = Depends(get_db)) -> ComisionService:
    event_manager = get_event_manager()
    return ComisionService(db, event_manager)

@router.post("/reservar", response_model=ApiResponse, status_code=status.HTTP_202_ACCEPTED)
async def reservar_comision(
    request: ReservarComisionRequest,
    servicio: ComisionService = Depends(get_comision_service)
):
    try:
        resultado = await servicio.reservar_comision(
            id_interaccion=request.id_interaccion,
            id_campania=request.id_campania,
            tipo_interaccion=request.tipo_interaccion,
            valor_interaccion=request.valor_interaccion,
            moneda_interaccion=request.moneda_interaccion,
            fraud_ok=request.fraud_ok,
            score_fraude=request.score_fraude,
            parametros_adicionales=request.parametros_adicionales or {}
        )
        
        return ApiResponse(
            exitoso=True,
            mensaje="Comisión reservada exitosamente",
            data={"id_comision": str(resultado.id) if resultado else None}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/confirmar/{comision_id}", response_model=ApiResponse)
async def confirmar_comision(
    comision_id: UUID,
    request: ConfirmarComisionRequest,
    servicio: ComisionService = Depends(get_comision_service)
):
    try:
        resultado = await servicio.confirmar_comision(
            id_comision=comision_id,
            lote_confirmacion=request.lote_confirmacion,
            referencia_pago=request.referencia_pago
        )
        
        return ApiResponse(
            exitoso=True,
            mensaje="Comisión confirmada exitosamente",
            data={
                "id_comision": str(resultado.id),
                "estado": resultado.estado.value
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/confirmar-lote", response_model=ApiResponse)
async def confirmar_comisiones_lote(
    request: ConfirmarLoteRequest,
    servicio: ComisionService = Depends(get_comision_service)
):
    try:
        resultado = await servicio.confirmar_comisiones_en_lote(
            limite_comisiones=request.limite_comisiones,
            lote_id=request.lote_id
        )
        
        return ApiResponse(
            exitoso=True,
            mensaje=f"Lote procesado: {resultado['cantidad_confirmadas']} comisiones confirmadas",
            data={
                "lote_id": resultado['lote_id'],
                "cantidad_confirmadas": resultado['cantidad_confirmadas'],
                "comisiones": [str(comision.id) for comision in resultado['comisiones']]
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/revertir/{comision_id}", response_model=ApiResponse)
async def revertir_comision(
    comision_id: UUID,
    request: RevertirComisionRequest,
    servicio: ComisionService = Depends(get_comision_service)
):
    try:
        resultado = await servicio.revertir_comision(
            id_comision=comision_id,
            motivo=request.motivo
        )
        
        return ApiResponse(
            exitoso=True,
            mensaje="Comisión revertida exitosamente",
            data={
                "id_comision": str(resultado.id),
                "estado": resultado.estado.value,
                "motivo": request.motivo
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{comision_id}", response_model=ComisionResponse)
async def obtener_comision(
    comision_id: UUID,
    servicio: ComisionService = Depends(get_comision_service)
):
    try:
        comision = await servicio.obtener_comision_por_id(comision_id)
        
        if not comision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comisión {comision_id} no encontrada"
            )
        
        return ComisionResponse(
            id=comision.id,
            id_interaccion=comision.id_interaccion,
            id_campania=comision.id_campania,
            monto_valor=comision.monto.valor,
            monto_moneda=comision.monto.moneda,
            estado=comision.estado.value,
            fecha_creacion=comision.fecha_creacion,
            fecha_actualizacion=comision.fecha_actualizacion,
            fecha_vencimiento=comision.fecha_vencimiento
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("", response_model=List[ComisionResponse])
async def listar_comisiones(
    estado: Optional[str] = None,
    id_campania: Optional[UUID] = None,
    para_lote: bool = False,
    limite: int = 100,
    servicio: ComisionService = Depends(get_comision_service)
):
    try:
        comisiones = await servicio.listar_comisiones(
            estado=estado,
            id_campania=id_campania,
            para_lote=para_lote,
            limite=limite
        )
        
        return [
            ComisionResponse(
                id=comision.id,
                id_interaccion=comision.id_interaccion,
                id_campania=comision.id_campania,
                monto_valor=comision.monto.valor,
                monto_moneda=comision.monto.moneda,
                estado=comision.estado.value,
                fecha_creacion=comision.fecha_creacion,
                fecha_actualizacion=comision.fecha_actualizacion,
                fecha_vencimiento=comision.fecha_vencimiento
            )
            for comision in comisiones
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/estadisticas", response_model=dict)
async def estadisticas_comisiones(
    id_campania: Optional[UUID] = None,
    servicio: ComisionService = Depends(get_comision_service)
):
    try:
        estadisticas = await servicio.obtener_estadisticas_comisiones(id_campania)
        
        return {
            "total_comisiones": estadisticas["total_comisiones"],
            "por_estado": {
                "reservadas": estadisticas["reservadas"],
                "confirmadas": estadisticas["confirmadas"],
                "revertidas": estadisticas["revertidas"],
                "canceladas": estadisticas["canceladas"]
            },
            "montos": {
                "total_reservado": str(estadisticas["monto_total_reservado"]),
                "total_confirmado": str(estadisticas["monto_total_confirmado"]),
                "total_revertido": str(estadisticas["monto_total_revertido"])
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
