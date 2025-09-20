from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Any

from .schemas import CrearCampaniaRequest, CrearCampaniaResponse, ActivarCampaniaResponse, ErrorResponse
from bff_web.despachadores import DespachadorMarketing

router = APIRouter()

@router.post("/campanias", response_model=CrearCampaniaResponse, responses={400: {"model": ErrorResponse}})
async def crear_campania(campania: CrearCampaniaRequest, background_tasks: BackgroundTasks):
    try:
        datos_campania = {
            "nombre": campania.nombre,
            "descripcion": campania.descripcion,
            "fecha_inicio": campania.fecha_inicio,
            "fecha_fin": campania.fecha_fin,
            "tipo": campania.tipo,
            "edad_minima": campania.edad_minima,
            "edad_maxima": campania.edad_maxima,
            "genero": campania.genero,
            "ubicacion": campania.ubicacion,
            "intereses": campania.intereses,
            "presupuesto": campania.presupuesto,
            "canales": campania.canales
        }

        despachador = DespachadorMarketing()
        background_tasks.add_task(despachador.publicar_comando_crear_campania, datos_campania)

        return CrearCampaniaResponse()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando comando de creación: {str(e)}")

@router.put("/campanias/{campania_id}/activar", response_model=ActivarCampaniaResponse, responses={400: {"model": ErrorResponse}})
async def activar_campania(campania_id: str, background_tasks: BackgroundTasks):
    try:
        despachador = DespachadorMarketing()
        background_tasks.add_task(despachador.publicar_comando_activar_campania, campania_id)

        return ActivarCampaniaResponse()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando comando de activación: {str(e)}")