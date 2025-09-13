from uuid import UUID
from atribucion.seedwork.dominio.repositorios import Mapeador
from atribucion.modulos.atribucion.dominio.entidades import Journey, Touchpoint, EstadoJourney
from .dto import Journey as JourneyDTO, Touchpoint as TouchpointDTO
from datetime import datetime

class MapeadorJourneySQLite(Mapeador):

    def obtener_tipo(self) -> type:
        return Journey.__class__

    def entidad_a_dto(self, entidad: Journey) -> JourneyDTO:
        journey_dto = JourneyDTO(
            id=str(entidad.id),
            usuario_id=entidad.usuario_id,
            estado=entidad.estado,
            fecha_inicio=entidad.fecha_inicio,
            fecha_ultima_actividad=entidad.fecha_ultima_actividad
        )
        
        journey_dto.touchpoints = []
        for touchpoint_entidad in entidad.touchpoints:
            touchpoint_dto = TouchpointDTO(
                id=str(uuid.uuid4()), 
                orden=touchpoint_entidad.orden,
                timestamp=touchpoint_entidad.timestamp,
                campania_id=touchpoint_entidad.campania_id,
                canal=touchpoint_entidad.canal,
                tipo_interaccion=touchpoint_entidad.tipo_interaccion
            )
            journey_dto.touchpoints.append(touchpoint_dto)
            
        return journey_dto

    def dto_a_entidad(self, dto: JourneyDTO) -> Journey:
        journey = Journey(
            id=UUID(dto.id),
            usuario_id=dto.usuario_id,
            estado=dto.estado,
            fecha_inicio=dto.fecha_inicio,
            fecha_ultima_actividad=dto.fecha_ultima_actividad
        )
        
        journey.touchpoints = []
        for touchpoint_dto in dto.touchpoints:
            touchpoint_entidad = Touchpoint(
                orden=touchpoint_dto.orden,
                timestamp=touchpoint_dto.timestamp,
                campania_id=touchpoint_dto.campania_id,
                canal=touchpoint_dto.canal,
                tipo_interaccion=touchpoint_dto.tipo_interaccion
            )
            journey.touchpoints.append(touchpoint_entidad)

        return journey



class MapeadorJourneyMongoDB(Mapeador):
    
    def obtener_tipo(self) -> type:
        return Journey.__class__

    def entidad_a_dto(self, entidad: Journey) -> dict:
        
        touchpoints_dict = [
            {
                "orden": tp.orden,
                "timestamp": tp.timestamp,
                "campania_id": tp.campania_id,
                "canal": tp.canal,
                "tipo_interaccion": tp.tipo_interaccion
            } for tp in entidad.touchpoints
        ]
        
        return {
            "_id": str(entidad.id),
            "usuario_id": entidad.usuario_id,
            "estado": entidad.estado.value,
            "fecha_inicio": entidad.fecha_inicio,
            "fecha_ultima_actividad": entidad.fecha_ultima_actividad,
            "touchpoints": touchpoints_dict,
            "fecha_actualizacion": datetime.utcnow()
        }

    def dto_a_entidad(self, dto: dict) -> Journey:
        
        touchpoints_entidad = [
            Touchpoint(
                orden=tp_dict.get('orden'),
                timestamp=tp_dict.get('timestamp'),
                campania_id=tp_dict.get('campania_id'),
                canal=tp_dict.get('canal'),
                tipo_interaccion=tp_dict.get('tipo_interaccion')
            ) for tp_dict in dto.get('touchpoints', [])
        ]
        
        journey = Journey(
            id=UUID(dto.get('_id')),
            usuario_id=dto.get('usuario_id'),
            estado=EstadoJourney(dto.get('estado')),
            fecha_inicio=dto.get('fecha_inicio'),
            fecha_ultima_actividad=dto.get('fecha_ultima_actividad'),
            touchpoints=touchpoints_entidad
        )
        
        return journey