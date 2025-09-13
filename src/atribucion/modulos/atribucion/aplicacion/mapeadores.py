from atribucion.seedwork.aplicacion.dto import DTO, Mapeador as AppMap
from atribucion.seedwork.dominio.repositorios import Mapeador as RepMap
from atribucion.modulos.atribucion.dominio.entidades import Journey, Touchpoint
from .dto import AtribucionDTO, IdentidadUsuarioDTO, ParametrosTrackingDTO, ElementoObjetivoDTO, ContextoInteraccionDTO
from datetime import datetime, timezone

class MapeadorAtribucion(RepMap):
    def obtener_tipo(self) -> type:
        return Journey.__class__

    def entidad_a_dto(self, entidad: Journey) -> AtribucionDTO:
        raise NotImplementedError

    def dto_a_entidad(self, dto: AtribucionDTO) -> Journey:
        journey = Journey(
            usuario_id=dto.identidad_usuario.id_usuario,
        )

        timestamp_obj = datetime.fromtimestamp(dto.marca_temporal / 1000, tz=timezone.utc)
        primer_touchpoint = Touchpoint(
            orden=1,
            timestamp=timestamp_obj,
            campania_id=dto.parametros_tracking.campania,
            afiliado_id=dto.parametros_tracking.id_afiliado, 
            canal=dto.parametros_tracking.medio,
            tipo_interaccion=dto.tipo
        )
        
        journey.touchpoints.append(primer_touchpoint)
        
        return journey


class MapeadorAtribucionDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> AtribucionDTO:
        
        identidad_usuario_dto = IdentidadUsuarioDTO(
            **externo.get('identidad_usuario', {})
        )
        parametros_tracking_dto = ParametrosTrackingDTO(
            **externo.get('parametros_tracking', {})
        )
        elemento_objetivo_dto = ElementoObjetivoDTO(
            **externo.get('elemento_objetivo', {})
        )
        contexto_dto = ContextoInteraccionDTO(
            **externo.get('contexto', {})
        )
        
        atribucion_dto = AtribucionDTO(
            id_interaccion=externo.get('id_interaccion'),
            tipo=externo.get('tipo'),
            marca_temporal=externo.get('marca_temporal'),
            identidad_usuario=identidad_usuario_dto,
            parametros_tracking=parametros_tracking_dto,
            elemento_objetivo=elemento_objetivo_dto,
            contexto=contexto_dto
        )
        return atribucion_dto

    def dto_a_externo(self, dto: DTO) -> dict:
        from dataclasses import asdict
        return asdict(dto)
