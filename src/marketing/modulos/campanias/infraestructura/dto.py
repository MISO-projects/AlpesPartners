from marketing.config.db import db
from sqlalchemy import Column, String, DateTime, Float, Integer, Text, JSON


class CampaniaDbDto(db.Model):
    __tablename__ = "campanias"
    
    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    estado = Column(String)
    tipo = Column(String)
    
    segmento = Column(JSON)
    
    configuracion = Column(JSON)
    
    metricas = Column(JSON)
    
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)
