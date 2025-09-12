from dataclasses import dataclass
from tracking.seedwork.aplicacion.dto import DTO
from datetime import datetime


@dataclass(frozen=True)
class IdentidadUsuarioDTO(DTO):
    id_usuario: str
    id_anonimo: str
    direccion_ip: str
    agente_usuario: str


@dataclass(frozen=True)
class ParametrosTrackingDTO(DTO):
    fuente: str
    medio: str
    campania: str
    contenido: str
    termino: str
    id_afiliado: str


@dataclass(frozen=True)
class ElementoObjetivoDTO(DTO):
    id_elemento: str
    tipo_elemento: str
    nombre_elemento: str
    url_elemento: str
    texto_elemento: str
    imagen_elemento: str
    video_elemento: str
    audio_elemento: str
    link_elemento: str
    texto_alternativo_elemento: str
    titulo_elemento: str


@dataclass(frozen=True)
class ContextoInteraccionDTO(DTO):
    url_pagina: str
    url_referente: str
    informacion_dispositivo: str


@dataclass(frozen=True)
class InteraccionDTO(DTO):
    tipo: str
    marca_temporal: datetime
    identidad_usuario: IdentidadUsuarioDTO
    parametros_tracking: ParametrosTrackingDTO
    elemento_objetivo: ElementoObjetivoDTO
    contexto: ContextoInteraccionDTO
