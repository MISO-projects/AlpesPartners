from tracking.config.db import db
from tracking.seedwork.infraestructura.uow import UnidadTrabajo, Batch
import os


class UnidadTrabajoSQLAlchemy(UnidadTrabajo):

    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        return list[db.session.get_nested_transaction()]

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    def commit(self):
        for batch in self.batches:
            lock = batch.lock
            batch.operacion(*batch.args, **batch.kwargs)

        db.session.commit()

        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db.session.rollback()

        super().rollback()

    def savepoint(self):
        db.session.begin_nested()


class UnidadTrabajoMongoDB(UnidadTrabajo):
    """
    MongoDB Unit of Work implementation that's pickle-safe
    No MongoDB client references to avoid pickle issues
    """

    def __init__(self):
        self._batches: list[Batch] = list()
        # Absolutely no MongoDB client/session references stored

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        # MongoDB doesn't have savepoints like SQL databases
        return []

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    def commit(self):
        """
        Execute all batched operations immediately
        MongoDB is designed for high-throughput writes, so we don't need complex transaction management
        """
        try:
            for batch in self.batches:
                # Execute the operation directly - the repository handles MongoDB connection
                batch.operacion(*batch.args, **batch.kwargs)
            
            super().commit()
        except Exception as e:
            print(f"Error during MongoDB commit: {e}")
            super().rollback()
            raise

    def rollback(self, savepoint=None):
        """
        MongoDB doesn't support traditional rollback
        We just clear the batches and call parent rollback for event cleanup
        """
        super().rollback()

    def savepoint(self):
        """
        MongoDB doesn't support savepoints - no-op for compatibility
        """
        pass


def get_unit_of_work() -> UnidadTrabajo:
    """Factory function to get the appropriate Unit of Work based on database type"""
    database_type = os.getenv('DATABASE_TYPE', 'mongodb').lower()
    
    if database_type == 'mongodb':
        return UnidadTrabajoMongoDB()
    else:
        return UnidadTrabajoSQLAlchemy()