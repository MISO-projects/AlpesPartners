from tracking.config.db import db
from sqlalchemy import Column, String, DateTime

Base = db.declarative_base()


class InteraccionDbDto(db.Model):
    __tablename__ = "interacciones"
    id = Column(String, primary_key=True)
    tipo = Column(String)
    marca_temporal = Column(DateTime)
    identidad_usuario = Column(String)
    parametros_tracking = Column(String)
    elemento_objetivo = Column(String)
    contexto = Column(String)
    estado = Column(String)
