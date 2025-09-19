from tracking.seedwork.dominio.repositorios import Mapeador as RepMap
from tracking.modulos.interacciones.aplicacion.dto import (
    InteraccionDTO,
)
from tracking.modulos.interacciones.dominio.entidades import Interaccion
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
        return Interaccion(
            tipo=dto.tipo,
            marca_temporal=datetime.strptime(dto.marca_temporal, self._FORMATO_FECHA),
            identidad_usuario=dto.identidad_usuario,
            parametros_tracking=dto.parametros_tracking,
            elemento_objetivo=dto.elemento_objetivo,
            contexto=dto.contexto,
            estado=dto.estado,
        )
