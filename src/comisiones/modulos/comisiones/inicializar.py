
from alpespartners.config.db import db
from alpespartners.modulos.comisiones.infraestructura.dto import (
    ComisionDbDto,
    ConfiguracionComisionDbDto,
    PoliticaFraudeDbDto,
    LoteComisionDbDto
)
from alpespartners.modulos.comisiones.infraestructura.despachadores import registrar_despachadores
from alpespartners.modulos.comisiones.aplicacion.handlers import registrar_handlers
from alpespartners.modulos.comisiones.dominio.objetos_valor import TipoComision, TipoPoliticaFraude
from datetime import datetime
from decimal import Decimal
import uuid

def crear_tablas():

    try:
        db.create_all()
        print("Tablas del módulo de comisiones creadas exitosamente")
    except Exception as e:
        print(f"Error creando tablas de comisiones: {e}")
        raise e

def insertar_configuraciones_default():

    try:
        config_existente = db.session.query(ConfiguracionComisionDbDto).first()
        if config_existente:
            print(" Ya existen configuraciones de comisión")
            return
        config_default = ConfiguracionComisionDbDto(
            id=str(uuid.uuid4()),
            nombre="Configuración por defecto",
            descripcion="Configuración de comisión del 5% que aplica por defecto",
            tipo=TipoComision.PORCENTAJE.value,
            porcentaje=Decimal('5.0'),
            minimo_valor=Decimal('1.0'),
            minimo_moneda='USD',
            maximo_valor=Decimal('1000.0'),
            maximo_moneda='USD',
            activo=True
        )
        config_compras = ConfiguracionComisionDbDto(
            id=str(uuid.uuid4()),
            nombre="Comisión para compras",
            descripcion="Configuración de comisión del 10% para interacciones de tipo PURCHASE",
            tipo=TipoComision.PORCENTAJE.value,
            porcentaje=Decimal('10.0'),
            tipo_interaccion="PURCHASE",
            minimo_valor=Decimal('5.0'),
            minimo_moneda='USD',
            maximo_valor=Decimal('5000.0'),
            maximo_moneda='USD',
            activo=True
        )
        config_leads = ConfiguracionComisionDbDto(
            id=str(uuid.uuid4()),
            nombre="Comisión fija para leads",
            descripcion="Comisión fija de $25 USD para leads",
            tipo=TipoComision.FIJO.value,
            monto_fijo_valor=Decimal('25.0'),
            monto_fijo_moneda='USD',
            tipo_interaccion="LEAD",
            activo=True
        )

        db.session.add(config_default)
        db.session.add(config_compras)
        db.session.add(config_leads)
        db.session.commit()

        print("Configuraciones por defecto de comisión insertadas")

    except Exception as e:
        db.session.rollback()
        print(f"Error insertando configuraciones por defecto: {e}")
        raise e

def insertar_politicas_fraude_default():

    try:
        politica_existente = db.session.query(PoliticaFraudeDbDto).first()
        if politica_existente:
            print(" Ya existen políticas de fraude")
            return
        politica_moderada = PoliticaFraudeDbDto(
            id=str(uuid.uuid4()),
            nombre="Política moderada",
            descripcion="Política de fraude moderada que rechaza interacciones con score > 50",
            tipo=TipoPoliticaFraude.MODERATE.value,
            threshold_score=50,
            requiere_revision_manual=False,
            tiempo_espera_minutos=0,
            activo=True
        )
        politica_estricta = PoliticaFraudeDbDto(
            id=str(uuid.uuid4()),
            nombre="Política estricta",
            descripción="Política estricta que rechaza interacciones con score > 30",
            tipo=TipoPoliticaFraude.STRICT.value,
            threshold_score=30,
            requiere_revision_manual=True,
            tiempo_espera_minutos=60,
            activo=True
        )
        politica_permisiva = PoliticaFraudeDbDto(
            id=str(uuid.uuid4()),
            nombre="Política permisiva",
            descripcion="Política permisiva que rechaza solo interacciones con score > 80",
            tipo=TipoPoliticaFraude.PERMISSIVE.value,
            threshold_score=80,
            requiere_revision_manual=False,
            tiempo_espera_minutos=0,
            activo=True
        )

        db.session.add(politica_moderada)
        db.session.add(politica_estricta)
        db.session.add(politica_permisiva)
        db.session.commit()

        print("Políticas por defecto de fraude insertadas")

    except Exception as e:
        db.session.rollback()
        print(f"Error insertando políticas por defecto: {e}")
        raise e

def registrar_event_handlers():

    try:
        # Usar el UoW local del módulo de comisiones
        from config.uow import inicializar_uow
        inicializar_uow()
        
        registrar_handlers()
        registrar_despachadores()
        print("Handlers y despachadores de eventos registrados correctamente")
    except Exception as e:
        print(f"Error registrando handlers: {e}")
        raise e

def inicializar_modulo_comisiones():

    print("Inicializando módulo de comisiones...")
    
    try:
        crear_tablas()
        insertar_configuraciones_default()
        insertar_politicas_fraude_default()
        registrar_event_handlers()
        
        print("Módulo de comisiones inicializado exitosamente")
        
    except Exception as e:
        print(f"Error inicializando módulo de comisiones: {e}")
        raise e

def limpiar_datos_prueba():

    try:
        print("Limpiando datos de comisiones...")
        db.session.query(ComisionDbDto).delete()
        db.session.query(LoteComisionDbDto).delete()
        
        db.session.commit()
        print("Datos de comisiones limpiados")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error limpiando datos: {e}")
        raise e

def crear_datos_ejemplo():

    try:
        print("Creando datos de ejemplo...")

        print("Datos de ejemplo creados")
        
    except Exception as e:
        print(f"Error creando datos de ejemplo: {e}")
        raise e

if __name__ == "__main__":
    inicializar_modulo_comisiones()
