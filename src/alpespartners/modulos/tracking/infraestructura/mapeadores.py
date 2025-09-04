from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.tracking.dominio.entidades import Interaccion
from alpespartners.modulos.tracking.infraestructura.dto import InteraccionDbDto


class MapeadorInteraccion(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Interaccion.__class__

    def entidad_a_dto(self, entidad: Interaccion) -> InteraccionDbDto:
        return InteraccionDbDto(
            id=str(entidad.id),
            tipo=entidad.tipo,
            marca_temporal=entidad.marca_temporal,
            # identidad_usuario=entidad.identidad_usuario,
            # parametros_tracking=entidad.parametros_tracking,
            # elemento_objetivo=entidad.elemento_objetivo,
            # contexto=entidad.contexto,
            identidad_usuario="temp",
            parametros_tracking="temp",
            elemento_objetivo="temp",
            contexto="temp",
        )

    def dto_a_entidad(self, dto: InteraccionDbDto) -> Interaccion:
        return Interaccion(
            tipo=dto.tipo,
            marca_temporal=dto.marca_temporal,
            identidad_usuario=dto.identidad_usuario,
            parametros_tracking=dto.parametros_tracking,
            elemento_objetivo=dto.elemento_objetivo,
            contexto=dto.contexto,
        )
