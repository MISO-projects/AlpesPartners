from fastapi import APIRouter, HTTPException
import httpx
from typing import Any

from .schemas import RegistrarInteraccionRequest, RegistrarInteraccionResponse, ErrorResponse

router = APIRouter()

TRACKING_SERVICE_URL = "http://tracking:8000"

@router.post("/interaccion", response_model=RegistrarInteraccionResponse, responses={400: {"model": ErrorResponse}})
async def registrar_interaccion(interaccion: RegistrarInteraccionRequest):
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "tipo": interaccion.tipo,
                "marca_temporal": interaccion.marca_temporal.isoformat(),
                "identidad_usuario": interaccion.identidad_usuario,
                "parametros_tracking": interaccion.parametros_tracking,
                "elemento_objetivo": interaccion.elemento_objetivo,
                "contexto": interaccion.contexto
            }

            response = await client.post(f"{TRACKING_SERVICE_URL}/interaccion", json=payload)

            if response.status_code == 202:
                return RegistrarInteraccionResponse()
            else:
                error_data = response.json() if response.headers.get("content-type") == "application/json" else {"error": "Error desconocido"}
                raise HTTPException(status_code=response.status_code, detail=error_data.get("error", "Error en el servicio de tracking"))

        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Error de conexión con el servicio de tracking: {str(e)}")