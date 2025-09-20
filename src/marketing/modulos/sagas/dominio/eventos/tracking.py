import uuid
from dataclasses import dataclass
from marketing.seedwork.dominio.eventos import EventoDominio
from marketing.seedwork.dominio.objetos_valor import ObjetoValor
from typing import Optional
from datetime import datetime


@dataclass
class InteraccionesDescartadas(EventoDominio):
    id_correlacion: str = None
    interacciones: list[uuid.UUID] = None


@dataclass(frozen=True)
class ParametrosTracking(ObjetoValor):
    fuente: str
    medio: str
    campania: str
    contenido: str
    termino: str
    id_afiliado: str


@dataclass(frozen=True)
class IdentidadUsuario(ObjetoValor):
    id_usuario: Optional[str] = None
    id_anonimo: Optional[str] = None
    direccion_ip: Optional[str] = None
    agente_usuario: Optional[str] = None


@dataclass(frozen=True)
class ElementoObjetivo(ObjetoValor):
    url: str
    id_elemento: Optional[str] = None


@dataclass(frozen=True)
class ContextoInteraccion(ObjetoValor):
    url_pagina: str
    url_referente: Optional[str] = None
    informacion_dispositivo: Optional[str] = None


@dataclass
class InteraccionRegistrada(EventoDominio):
    id_correlacion: str = None
    id_interaccion: uuid.UUID = None
    tipo: str = None
    marca_temporal: datetime = None
    identidad_usuario: IdentidadUsuario = None
    parametros_tracking: ParametrosTracking = None
    elemento_objetivo: ElementoObjetivo = None
    contexto: ContextoInteraccion = None
    estado: str = None
