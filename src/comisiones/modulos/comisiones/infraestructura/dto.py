
from sqlalchemy import Column, String, DateTime, Text, Integer, Numeric, Boolean
from sqlalchemy.dialects.sqlite import JSON
from comisiones.config.db import Base
from datetime import datetime

class ComisionDbDto(Base):

    __tablename__ = 'comisiones'

    id = Column(String(64), primary_key=True)
    id_interaccion = Column(String(64), nullable=False, index=True)
    id_campania = Column(String(64), nullable=False, index=True)
    
    monto_valor = Column(Numeric(15, 4), nullable=False)
    monto_moneda = Column(String(3), nullable=False, default='USD')
    
    estado = Column(String(20), nullable=False, index=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_vencimiento = Column(DateTime, nullable=True)
    
    configuracion = Column(JSON, nullable=True)
    
    politica_fraude = Column(JSON, nullable=True)
    
    detalles_reserva = Column(JSON, nullable=True)
    
    detalles_confirmacion = Column(JSON, nullable=True)

    def __repr__(self):
        return f'<ComisionDbDto {self.id}>'

class ConfiguracionComisionDbDto(Base):

    __tablename__ = 'configuraciones_comision'

    id = Column(String(64), primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    
    tipo = Column(String(20), nullable=False)
    
    porcentaje = Column(Numeric(5, 4), nullable=True)
    monto_fijo_valor = Column(Numeric(15, 4), nullable=True)
    monto_fijo_moneda = Column(String(3), nullable=True)
    
    minimo_valor = Column(Numeric(15, 4), nullable=True)
    minimo_moneda = Column(String(3), nullable=True)
    maximo_valor = Column(Numeric(15, 4), nullable=True)
    maximo_moneda = Column(String(3), nullable=True)
    
    escalones = Column(JSON, nullable=True)
    id_campania = Column(String(64), nullable=True, index=True)
    tipo_interaccion = Column(String(50), nullable=True, index=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ConfiguracionComisionDbDto {self.nombre}>'

class PoliticaFraudeDbDto(Base):

    __tablename__ = 'politicas_fraude'

    id = Column(String(64), primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(20), nullable=False)
    threshold_score = Column(Integer, nullable=False, default=50)
    requiere_revision_manual = Column(Boolean, default=False)
    tiempo_espera_minutos = Column(Integer, default=0)
    id_campania = Column(String(64), nullable=True, index=True)

    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PoliticaFraudeDbDto {self.nombre}>'

class LoteComisionDbDto(Base):

    __tablename__ = 'lotes_comision'

    id = Column(String(64), primary_key=True)
    id_lote = Column(String(100), nullable=False, unique=True, index=True)
    cantidad_comisiones = Column(Integer, nullable=False)
    monto_total_valor = Column(Numeric(15, 4), nullable=False)
    monto_total_moneda = Column(String(3), nullable=False)
    estado = Column(String(20), nullable=False, default='PROCESANDO')
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_confirmacion = Column(DateTime, nullable=True)
    fecha_procesamiento = Column(DateTime, nullable=True)
    datos_adicionales = Column(JSON, nullable=True)

    def __repr__(self):
        return f'<LoteComisionDbDto {self.id_lote}>'
