from dataclasses import dataclass, field
from datetime import datetime
from marketing.seedwork.dominio.entidades import Entidad


@dataclass
class SagaLog(Entidad):
    id_correlacion: str = field(default="")
    tipo_paso: str = field(default="")
    evento: str = field(default="")
    comando: str = field(default="")
    estado: str = field(default="")
    timestamp: datetime = field(default=datetime.now())
    datos_adicionales: dict = field(default_factory=dict)
