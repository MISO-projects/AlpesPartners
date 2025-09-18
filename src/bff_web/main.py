from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from typing import Any
import httpx
import asyncio
from contextlib import asynccontextmanager

from .api.v1.router import router as v1

class Config(BaseSettings):
    APP_VERSION: str = "1"
    MARKETING_SERVICE_URL: str = "http://marketing:8000"
    TRACKING_SERVICE_URL: str = "http://tracking:8000"

settings = Config()
app_configs: dict[str, Any] = {"title": "BFF AlpesPartners"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan, **app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "BFF AlpesPartners"}