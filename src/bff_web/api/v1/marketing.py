from fastapi import APIRouter, HTTPException
import httpx
from typing import Any

from .schemas import CrearCampaniaRequest, CrearCampaniaResponse, ActivarCampaniaResponse, ErrorResponse

router = APIRouter()

MARKETING_SERVICE_URL = "http://marketing:8000"

@router.post("/campanias", response_model=CrearCampaniaResponse, responses={400: {"model": ErrorResponse}})
async def crear_campania(campania: CrearCampaniaRequest):
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "nombre": campania.nombre,
                "descripcion": campania.descripcion,
                "fecha_inicio": campania.fecha_inicio.isoformat(),
                "fecha_fin": campania.fecha_fin.isoformat(),
                "tipo": campania.tipo,
                "edad_minima": campania.edad_minima,
                "edad_maxima": campania.edad_maxima,
                "genero": campania.genero,
                "ubicacion": campania.ubicacion,
                "intereses": campania.intereses,
                "presupuesto": campania.presupuesto,
                "canales": campania.canales
            }

            response = await client.post(f"{MARKETING_SERVICE_URL}/campanias", json=payload)

            if response.status_code == 202:
                return CrearCampaniaResponse()
            else:
                error_data = response.json() if response.headers.get("content-type") == "application/json" else {"error": "Error desconocido"}
                raise HTTPException(status_code=response.status_code, detail=error_data.get("error", "Error en el servicio de marketing"))

        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Error de conexión con el servicio de marketing: {str(e)}")

@router.put("/campanias/{campania_id}/activar", response_model=ActivarCampaniaResponse, responses={400: {"model": ErrorResponse}})
async def activar_campania(campania_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{MARKETING_SERVICE_URL}/campanias/{campania_id}/activar")

            if response.status_code == 202:
                return ActivarCampaniaResponse()
            else:
                error_data = response.json() if response.headers.get("content-type") == "application/json" else {"error": "Error desconocido"}
                raise HTTPException(status_code=response.status_code, detail=error_data.get("error", "Error en el servicio de marketing"))

        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Error de conexión con el servicio de marketing: {str(e)}")