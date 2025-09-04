from dataclasses import dataclass
from typing import Optional
from alpespartners.seedwork.dominio.objetos_valor import ObjetoValor


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
