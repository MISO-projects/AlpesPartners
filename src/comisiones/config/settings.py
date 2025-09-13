
import os
from typing import Optional
from pydantic import BaseSettings, Field

class ComisionesSettings(BaseSettings):
    service_name: str = Field(default="comisiones", env="SERVICE_NAME")
    version: str = Field(default="1.0.0", env="SERVICE_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    database_url: str = Field(default="sqlite:///./comisiones.db", env="COMISIONES_DATABASE_URL")
    db_echo: bool = Field(default=False, env="DB_ECHO")
    pulsar_url: str = Field(default="pulsar://localhost:6650", env="PULSAR_URL")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8002, env="PORT")
    reload: bool = Field(default=True, env="RELOAD")
    batch_size_default: int = Field(default=100, env="COMISIONES_BATCH_SIZE")
    fraud_timeout_minutes: int = Field(default=15, env="COMISIONES_FRAUD_TIMEOUT")
    default_commission_percentage: float = Field(default=5.0, env="DEFAULT_COMMISSION_PERCENTAGE")
    fraud_threshold_default: int = Field(default=50, env="FRAUD_THRESHOLD_DEFAULT")
    fraud_review_threshold: int = Field(default=80, env="FRAUD_REVIEW_THRESHOLD")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")
    mongodb_url: Optional[str] = Field(default=None, env="MONGODB_URL")
    mongodb_database: str = Field(default="comisiones", env="MONGODB_DATABASE")
    allowed_origins: list = Field(default=["*"], env="ALLOWED_ORIGINS")
    allowed_methods: list = Field(default=["GET", "POST", "PUT", "DELETE"], env="ALLOWED_METHODS")
    allowed_headers: list = Field(default=["*"], env="ALLOWED_HEADERS")
    secret_key: str = Field(default="comisiones-secret-key-change-in-production", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=8003, env="METRICS_PORT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
settings = ComisionesSettings()

def get_settings():

    return settings
