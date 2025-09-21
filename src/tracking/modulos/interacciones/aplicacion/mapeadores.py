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
            id_usuario=dto.identidad_usuario.id_usuario,
            id_anonimo=dto.identidad_usuario.id_anonimo,
            direccion_ip=dto.identidad_usuario.direccion_ip,
            agente_usuario=dto.identidad_usuario.agente_usuario,
        )
        parametros_tracking = ParametrosTracking(
            fuente=dto.parametros_tracking.fuente,
            medio=dto.parametros_tracking.medio,
            campania=dto.parametros_tracking.campania,
            contenido=dto.parametros_tracking.contenido,
            termino=dto.parametros_tracking.termino,
            id_afiliado=dto.parametros_tracking.id_afiliado,
        )
        elemento_objetivo = ElementoObjetivo(
            url=dto.elemento_objetivo.url_elemento,
            id_elemento=dto.elemento_objetivo.id_elemento,
        )
        contexto = ContextoInteraccion(
            url_pagina=dto.contexto.url_pagina,
            url_referente=dto.contexto.url_referente,
            informacion_dispositivo=dto.contexto.informacion_dispositivo,
        )
        # Manejar marca_temporal que puede ser str o datetime
        if isinstance(dto.marca_temporal, str):
            marca_temporal = datetime.strptime(dto.marca_temporal, self._FORMATO_FECHA)
        else:
            marca_temporal = dto.marca_temporal

        return Interaccion(
            tipo=dto.tipo,
            marca_temporal=marca_temporal,
            identidad_usuario=identidad_usuario,
            parametros_tracking=parametros_tracking,
            elemento_objetivo=elemento_objetivo,
            contexto=contexto,
            estado=EstadoInteraccion(dto.estado),
        )
