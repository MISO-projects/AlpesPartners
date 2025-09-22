from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from typing import Any

from .schemas import ErrorResponse
from bff_web.schema import FraudeDetectadoPayload, EventoFraudeDetectadoIntegracion
from bff_web.despachadores import DespachadorMarketing

router = APIRouter()

class QueryParams(BaseModel):
    id_correlacion: str = Field(default="")

@router.get("/simular-fraude/{journey_id}", include_in_schema=False)
async def prueba_fraude_detectado(journey_id: str, q: QueryParams = Query()) -> dict[str, str]:
    id_correlacion = q.id_correlacion
    payload = FraudeDetectadoPayload(
        journey_id=journey_id,
        id_correlacion=id_correlacion,
    )

    evento = EventoFraudeDetectadoIntegracion(data=payload)
    despachador = DespachadorMarketing()
    despachador.publicar_mensaje_pulsar(evento, "fraude-detectado")
    return {"status": "ok", "journey_id": journey_id}