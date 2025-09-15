from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from tracking.seedwork.dominio.entidades import AgregacionRaiz
from tracking.modulos.interacciones.dominio.objetos_valor import (
    IdentidadUsuario,
    ParametrosTracking,
    ElementoObjetivo,
    ContextoInteraccion,
)
from tracking.modulos.interacciones.dominio.eventos import InteraccionRegistrada


@dataclass
class Interaccion(AgregacionRaiz):
    tipo: str = field(default="CLICK")
    marca_temporal: datetime = field(default=datetime.now())
    identidad_usuario: IdentidadUsuario = field(default_factory=IdentidadUsuario)
    parametros_tracking: ParametrosTracking = field(default_factory=ParametrosTracking)
    elemento_objetivo: ElementoObjetivo = field(default_factory=ElementoObjetivo)
    contexto: ContextoInteraccion = field(default_factory=ContextoInteraccion)

    def registrar_interaccion(
        self,
        interaccion: Interaccion,
    ):
        self.tipo = interaccion.tipo
        self.marca_temporal = interaccion.marca_temporal
        self.identidad_usuario = interaccion.identidad_usuario
        self.parametros_tracking = interaccion.parametros_tracking
        self.elemento_objetivo = interaccion.elemento_objetivo
        self.contexto = interaccion.contexto

        self.agregar_evento(
            InteraccionRegistrada(
                id_interaccion=self.id,
                tipo=interaccion.tipo,
                marca_temporal=interaccion.marca_temporal,
                identidad_usuario=interaccion.identidad_usuario,
                parametros_tracking=interaccion.parametros_tracking,
                elemento_objetivo=interaccion.elemento_objetivo,
                contexto=interaccion.contexto,
            )
        )
