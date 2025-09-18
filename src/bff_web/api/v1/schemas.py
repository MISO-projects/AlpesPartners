from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CrearCampaniaRequest(BaseModel):
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    tipo: Optional[str] = "DIGITAL"
    edad_minima: Optional[int] = None
    edad_maxima: Optional[int] = None
    genero: Optional[str] = None
    ubicacion: Optional[str] = None
    intereses: Optional[List[str]] = []
    presupuesto: Optional[float] = 0.0
    canales: Optional[List[str]] = ["WEB", "EMAIL"]

class CrearCampaniaResponse(BaseModel):
    message: str = "Campaña creada exitosamente"

class ActivarCampaniaResponse(BaseModel):
    message: str = "Campaña activada exitosamente"

class RegistrarInteraccionRequest(BaseModel):
    tipo: str
    marca_temporal: datetime
    identidad_usuario: str
    parametros_tracking: dict
    elemento_objetivo: str
    contexto: dict

class RegistrarInteraccionResponse(BaseModel):
    message: str = "Interacción registrada exitosamente"

class ErrorResponse(BaseModel):
    error: str