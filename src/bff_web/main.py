from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings
from typing import Any
import httpx
import asyncio
from contextlib import asynccontextmanager
from sse_starlette.sse import EventSourceResponse
import os

from .api.v1.router import router as v1
from .consumidores import suscribirse_a_eventos_campanias, suscribirse_a_eventos_activacion

class Config(BaseSettings):
    APP_VERSION: str = "1"
    MARKETING_SERVICE_URL: str = "http://marketing:8000"
    TRACKING_SERVICE_URL: str = "http://tracking:8000"

settings = Config()
app_configs: dict[str, Any] = {"title": "BFF AlpesPartners"}

# Listas globales para eventos
eventos_campanias = []
eventos_activacion = []
tasks = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar consumer de eventos de campañas en hilo separado
    import threading

    def consumer_campanias_thread():
        suscribirse_a_eventos_campanias(eventos_campanias)

    def consumer_activacion_thread():
        suscribirse_a_eventos_activacion(eventos_activacion)

    thread1 = threading.Thread(target=consumer_campanias_thread, daemon=True)
    thread2 = threading.Thread(target=consumer_activacion_thread, daemon=True)

    thread1.start()
    thread2.start()

    tasks.extend([thread1, thread2])

    yield

    # Los hilos daemon se cerrarán automáticamente

app = FastAPI(lifespan=lifespan, **app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1, prefix="/api/v1")

# Servir archivos estáticos
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def dashboard():
    """Servir la página principal del dashboard"""
    from fastapi.responses import FileResponse
    html_path = os.path.join(static_dir, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        return {"message": "Dashboard no disponible"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "BFF AlpesPartners"}

@app.get("/stream/campanias")
async def stream_eventos_campanias(request: Request):
    """
    Server-Sent Events endpoint que envía notificaciones cuando se crean campañas

    Uso desde JavaScript:
    const eventSource = new EventSource('/stream/campanias');
    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log('Campaña creada:', data);
    };
    """
    def nuevo_evento():
        global eventos_campanias, eventos_activacion
        import json

        # Priorizar eventos de creación
        if len(eventos_campanias) > 0:
            evento = eventos_campanias.pop(0)  # FIFO
            return {
                'data': json.dumps(evento),
                'event': 'campania_creada'
            }

        # Luego eventos de activación
        if len(eventos_activacion) > 0:
            evento = eventos_activacion.pop(0)  # FIFO
            return {
                'data': json.dumps(evento),
                'event': 'campania_activada'
            }

        return None

    async def generar_eventos():
        global eventos_campanias, eventos_activacion
        print(f"🔄 Cliente SSE conectado")

        while True:
            # Si el cliente cierra la conexión, salir
            if await request.is_disconnected():
                print("🔌 Cliente SSE desconectado")
                break

            # Si hay eventos, enviarlos
            if len(eventos_campanias) > 0 or len(eventos_activacion) > 0:
                evento = nuevo_evento()
                if evento:
                    yield evento

            # Esperar un poco antes del siguiente check
            await asyncio.sleep(0.5)

    return EventSourceResponse(generar_eventos())