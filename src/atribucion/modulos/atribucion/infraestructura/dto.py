# src/attribution/modulos/atribucion/infraestructura/dto.py
from atribucion.config.db import db
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from atribucion.modulos.atribucion.dominio.entidades import EstadoJourney

class Journey(db.Model):
    __tablename__ = "journeys"
    id = db.Column(db.String(40), primary_key=True)
    usuario_id = db.Column(db.String(40), nullable=False)
    estado = db.Column(SQLAlchemyEnum(EstadoJourney), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_ultima_actividad = db.Column(db.DateTime, nullable=False)
    
    touchpoints = relationship("Touchpoint", back_populates="journey")

class Touchpoint(db.Model):
    __tablename__ = "touchpoints"
    id = db.Column(db.String(40), primary_key=True)
    journey_id = db.Column(db.String(40), ForeignKey("journeys.id"), nullable=False)
    orden = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    campania_id = db.Column(db.String(40))
    canal = db.Column(db.String(40))
    tipo_interaccion = db.Column(db.String(40))

    journey = relationship("Journey", back_populates="touchpoints")