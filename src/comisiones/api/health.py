
from fastapi import APIRouter, status
from datetime import datetime
from comisiones.config.settings import get_settings
from comisiones.config.db import db
from comisiones.config.eventos import get_event_manager

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    settings = get_settings()
    
    return {
        "service": settings.service_name,
        "version": settings.version,
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check():
    settings = get_settings()
    
    health_status = {
        "service": settings.service_name,
        "version": settings.version,
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "dependencies": {}
    }
    
    try:
        session = db.get_session()
        session.execute("SELECT 1")
        health_status["dependencies"]["database"] = {
            "status": "healthy",
            "type": "SQLite" if "sqlite" in settings.database_url else "Other"
        }
    except Exception as e:
        health_status["dependencies"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    try:
        event_manager = get_event_manager()
        if event_manager.client:
            health_status["dependencies"]["events"] = {
                "status": "healthy",
                "type": "Pulsar"
            }
        else:
            health_status["dependencies"]["events"] = {
                "status": "disconnected",
                "type": "Pulsar"
            }
    except Exception as e:
        health_status["dependencies"]["events"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    return health_status

@router.get("/metrics", status_code=status.HTTP_200_OK)
async def metrics():
    return {
        "service": "comisiones",
        "metrics": {
            "uptime": "available",
            "requests_total": "N/A",
            "errors_total": "N/A",
            "database_connections": "N/A"
        }
    }
