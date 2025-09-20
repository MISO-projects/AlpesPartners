from marketing.config.db import db
from sqlalchemy import Column, String, DateTime, JSON


class SagaLogDTO(db.Model):
    __tablename__ = "sagas_logs"

    id = Column(String, primary_key=True)
    id_correlacion = Column(String, nullable=False, index=True)  # Add index for faster queries
    tipo_paso = Column(String, nullable=False)
    evento = Column(String, nullable=True)  # Allow null for commands-only entries
    comando = Column(String, nullable=True)  # Allow null for events-only entries
    estado = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    datos_adicionales = Column(JSON, nullable=True)  # Allow null
