from marketing.seedwork.dominio.repositorios import Mapeador
from marketing.modulos.sagas.dominio.entidades import SagaLog
from marketing.modulos.sagas.infraestructura.dto import SagaLogDTO
from uuid import UUID


class MapeadorSagaLogSQLite(Mapeador):
    def obtener_tipo(self) -> type:
        return SagaLog.__class__

    def entidad_a_dto(self, entidad: SagaLog) -> SagaLogDTO:
        return SagaLogDTO(
            id=str(entidad.id),
            id_correlacion=str(entidad.id_correlacion),  # Convert UUID to string
            tipo_paso=entidad.tipo_paso,
            evento=entidad.evento or "",  # Handle None values
            comando=entidad.comando or "",  # Handle None values
            estado=entidad.estado,
            timestamp=entidad.timestamp,
            datos_adicionales=entidad.datos_adicionales or {},  # Handle None values
        )

    def dto_a_entidad(self, dto: SagaLogDTO) -> SagaLog:
        return SagaLog(
            id=UUID(dto.id),
            id_correlacion=UUID(dto.id_correlacion),  # Convert string back to UUID
            tipo_paso=dto.tipo_paso,
            evento=dto.evento,
            comando=dto.comando,
            estado=dto.estado,
            timestamp=dto.timestamp,
            datos_adicionales=dto.datos_adicionales,
        )
