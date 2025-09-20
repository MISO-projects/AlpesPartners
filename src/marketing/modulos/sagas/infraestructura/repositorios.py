from marketing.modulos.sagas.dominio.repositorios import RepositorioSagaLog
from marketing.modulos.sagas.dominio.fabricas import FabricaSagaLog
from marketing.modulos.sagas.dominio.entidades import SagaLog
from uuid import UUID
from marketing.modulos.sagas.infraestructura.dto import SagaLogDTO
from marketing.modulos.sagas.infraestructura.mapeadores import MapeadorSagaLogSQLite
from marketing.config.db import db

class RepositorioSagaLogPostgres(RepositorioSagaLog):
    def __init__(self):
        self._fabrica_saga: FabricaSagaLog = FabricaSagaLog()
        self._mapeador = MapeadorSagaLogSQLite()

    @property
    def fabrica_saga(self) -> FabricaSagaLog:
        return self._fabrica_saga

    def obtener_todos(self, id_correlacion: UUID) -> list[SagaLog]:
        sagas_logs_dto = (
            db.session.query(SagaLogDTO)
            .filter_by(id_correlacion=str(id_correlacion))
            .order_by(SagaLogDTO.timestamp.asc())
            .all()
        )
        return [
            self._mapeador.dto_a_entidad(dto)
            for dto in sagas_logs_dto
        ]

    def agregar(self, saga: SagaLog):
        saga_log_dto = self._mapeador.entidad_a_dto(saga)
        db.session.add(saga_log_dto)
        # Note: No commit here, let the coordinator handle transaction management
