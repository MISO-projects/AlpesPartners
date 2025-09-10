from dataclasses import dataclass
from marketing.seedwork.aplicacion.dto import DTO
from datetime import datetime


@dataclass(frozen=True)
class SegmentoAudienciaDTO(DTO):
    edad_minima: int
    edad_maxima: int
    genero: str
    ubicacion: str
    intereses: list


@dataclass(frozen=True)
class ConfiguracionCampaniaDTO(DTO):
    presupuesto: float
    moneda: str
    canales: list
    frecuencia_maxima: int
    duracion_sesion_minutos: int


@dataclass(frozen=True)
class MetricasCampaniaDTO(DTO):
    impresiones: int
    clics: int
    conversiones: int
    costo_total: float


@dataclass(frozen=True)
class CampaniaDTO(DTO):
    id: str
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str
    tipo: str
    segmento: SegmentoAudienciaDTO
    configuracion: ConfiguracionCampaniaDTO
    metricas: MetricasCampaniaDTO
