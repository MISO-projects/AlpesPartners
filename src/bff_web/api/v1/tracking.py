from fastapi import APIRouter, HTTPException, BackgroundTasks
import uuid

from .schemas import RegistrarInteraccionRequest, RegistrarInteraccionResponse, ErrorResponse
from bff_web.despachadores import DespachadorTracking

router = APIRouter()

@router.post("/interaccion", response_model=RegistrarInteraccionResponse, responses={400: {"model": ErrorResponse}})
async def registrar_interaccion(interaccion: RegistrarInteraccionRequest, background_tasks: BackgroundTasks):
    try:
        # Formatear fecha para tracking (formato: YYYY-MM-DDTHH:MM:SSZ)
        fecha_formato_tracking = interaccion.marca_temporal.strftime('%Y-%m-%dT%H:%M:%SZ')

        datos_interaccion = {
            "tipo": interaccion.tipo,
            "marca_temporal": fecha_formato_tracking,
            "identidad_usuario": interaccion.identidad_usuario,
            "parametros_tracking": interaccion.parametros_tracking,
            "elemento_objetivo": interaccion.elemento_objetivo,
            "contexto": interaccion.contexto
        }

        despachador = DespachadorTracking()
        background_tasks.add_task(despachador.publicar_comando_registrar_interaccion, datos_interaccion)

        # Generar un ID de correlación único para la respuesta
        return RegistrarInteraccionResponse(id_correlacion=str(uuid.uuid4()))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando comando de interacción: {str(e)}")