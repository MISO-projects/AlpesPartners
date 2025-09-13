import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional
from atribucion.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class IdentidadUsuarioDTO(DTO):
    id_usuario: Optional[str] = None
    id_anonimo: Optional[str] = None
    direccion_ip: Optional[str] = None
    agente_usuario: Optional[str] = None

@dataclass(frozen=True)
class ParametrosTrackingDTO(DTO):
    fuente: str
    medio: str
    campania: str
    id_afiliado: str
    contenido: Optional[str] = None
    termino: Optional[str] = None
    

@dataclass(frozen=True)
class ElementoObjetivoDTO(DTO):
    url: str
    id_elemento: Optional[str] = None

@dataclass(frozen=True)
class ContextoInteraccionDTO(DTO):
    url_pagina: Optional[str] = None
    url_referente: Optional[str] = None
    informacion_dispositivo: Optional[str] = None


@dataclass(frozen=True)
class AtribucionDTO(DTO):
    id_interaccion: uuid.UUID
    tipo: str
    marca_temporal: int
    identidad_usuario: IdentidadUsuarioDTO
    parametros_tracking: ParametrosTrackingDTO
    elemento_objetivo: ElementoObjetivoDTO
    contexto: ContextoInteraccionDTO

    def to_dict(self) -> dict:
        """Convierte el DTO a un diccionario."""
        return asdict(self)