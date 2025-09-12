
import sys
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import get_settings
from config.db import get_db, db
from config.eventos import get_event_manager
from api.comisiones import router as comisiones_router
from api.health import router as health_router
from services.event_service import EventService
from modulos.comisiones.inicializar import inicializar_modulo_comisiones

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()
app = FastAPI(
    title="Servicio de Comisiones",
    description="Microservicio para gestión de comisiones de marketing",
    version=settings.version,
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

app.include_router(comisiones_router, prefix="/api/v1/comisiones", tags=["comisiones"])
app.include_router(health_router, prefix="/api/v1", tags=["health"])

event_service = None

@app.on_event("startup")
async def startup_event():
    global event_service
    
    try:
        logger.info("Iniciando servicio de comisiones...")
        
        logger.info("Inicializando base de datos...")
        db.create_tables()
        
        logger.info("Inicializando módulo de comisiones...")
        inicializar_modulo_comisiones()
        
        logger.info("Conectando a sistema de eventos...")
        event_manager = get_event_manager()
        if event_manager.connect():
            logger.info("Conectado al sistema de eventos")
        else:
            logger.warning("No se pudo conectar al sistema de eventos")
        
        event_service = EventService()
        await event_service.start()
        
        logger.info("Servicio de comisiones iniciado exitosamente")
        
    except Exception as e:
        logger.error(f"Error iniciando servicio: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    global event_service
    
    logger.info("Cerrando servicio de comisiones...")
    
    try:
        if event_service:
            await event_service.stop()
        
        event_manager = get_event_manager()
        event_manager.disconnect()
        
        db.close_session()
        
        logger.info("Servicio cerrado exitosamente")
        
    except Exception as e:
        logger.error(f"Error cerrando servicio: {e}")

@app.get("/")
async def root():
    return {
        "service": "comisiones",
        "version": settings.version,
        "status": "running",
        "description": "Microservicio de gestión de comisiones"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Error interno del servidor",
            "status_code": 500
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
