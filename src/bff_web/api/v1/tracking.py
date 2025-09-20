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
            # Formatear fecha para tracking (formato: YYYY-MM-DDTHH:MM:SSZ)
            fecha_formato_tracking = interaccion.marca_temporal.strftime('%Y-%m-%dT%H:%M:%SZ')

            # Adaptar formato para tracking service
            payload = {
                "tipo": interaccion.tipo,
                "marca_temporal": fecha_formato_tracking,
                "identidad_usuario": {
                    "id_usuario": interaccion.identidad_usuario,
                    "id_anonimo": None,
                    "direccion_ip": None,
                    "agente_usuario": None
                },
                "parametros_tracking": interaccion.parametros_tracking,
                "elemento_objetivo": {
                    "url": None,
                    "id_elemento": interaccion.elemento_objetivo
                },
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