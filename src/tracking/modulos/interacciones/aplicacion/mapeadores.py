from tracking.seedwork.dominio.repositorios import Mapeador as RepMap
from tracking.modulos.interacciones.aplicacion.dto import (
    InteraccionDTO,
)
from tracking.modulos.interacciones.dominio.entidades import Interaccion, EstadoInteraccion
from tracking.modulos.interacciones.dominio.objetos_valor import (
    IdentidadUsuario,
    ParametrosTracking,
    ElementoObjetivo,
    ContextoInteraccion,
)
from tracking.seedwork.aplicacion.dto import Mapeador as AppMap
from datetime import datetime


class MapeadorInteraccionDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> InteraccionDTO:
        return InteraccionDTO(
            tipo=externo["tipo"],
            marca_temporal=externo["marca_temporal"],
            identidad_usuario=externo["identidad_usuario"],
            parametros_tracking=externo["parametros_tracking"],
            elemento_objetivo=externo["elemento_objetivo"],
            contexto=externo["contexto"],
            estado=externo.get("estado", "REGISTRADA"),
        )

    def dto_a_externo(self, dto: InteraccionDTO) -> dict:
        return dto.__dict__


class MapeadorInteraccion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Interaccion.__class__

    def entidad_a_dto(self, entidad: Interaccion) -> InteraccionDTO:
        return InteraccionDTO(
            tipo=entidad.tipo,
            marca_temporal=entidad.marca_temporal,
            identidad_usuario=entidad.identidad_usuario,
            parametros_tracking=entidad.parametros_tracking,
            elemento_objetivo=entidad.elemento_objetivo,
            contexto=entidad.contexto,
            estado=entidad.estado,
        )

    def dto_a_entidad(self, dto: InteraccionDTO) -> Interaccion:
        identidad_usuario = IdentidadUsuario(
            id_usuario=dto.identidad_usuario.get("id_usuario"),
            id_anonimo=dto.identidad_usuario.get("id_anonimo"),
            direccion_ip=dto.identidad_usuario.get("direccion_ip"),
            agente_usuario=dto.identidad_usuario.get("agente_usuario"),
        )
        parametros_tracking = ParametrosTracking(
            fuente=dto.parametros_tracking.get("fuente"),
            medio=dto.parametros_tracking.get("medio"),
            campania=dto.parametros_tracking.get("campania"),
            contenido=dto.parametros_tracking.get("contenido"),
            termino=dto.parametros_tracking.get("termino"),
            id_afiliado=dto.parametros_tracking.get("id_afiliado"),
        )
        elemento_objetivo = ElementoObjetivo(
            url=dto.elemento_objetivo.get("url"),
            id_elemento=dto.elemento_objetivo.get("id_elemento"),
        )
        contexto = ContextoInteraccion(
            url_pagina=dto.contexto.get("url_pagina"),
            url_referente=dto.contexto.get("url_referente"),
            informacion_dispositivo=dto.contexto.get("informacion_dispositivo"),
        )
        return Interaccion(
            tipo=dto.tipo,
            marca_temporal=datetime.strptime(dto.marca_temporal, self._FORMATO_FECHA),
            identidad_usuario=identidad_usuario,
            parametros_tracking=parametros_tracking,
            elemento_objetivo=elemento_objetivo,
            contexto=contexto,
            estado=EstadoInteraccion(dto.estado),
        )
