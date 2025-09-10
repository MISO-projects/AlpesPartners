from dataclasses import dataclass
from typing import Optional, List
from marketing.seedwork.dominio.objetos_valor import ObjetoValor


@dataclass(frozen=True)
class SegmentoAudiencia(ObjetoValor):
    edad_minima: Optional[int] = None
    edad_maxima: Optional[int] = None
    genero: Optional[str] = None
    ubicacion: Optional[str] = None
    intereses: List[str] = None

    def __post_init__(self):
        if self.intereses is None:
            object.__setattr__(self, 'intereses', [])


@dataclass(frozen=True)
class ConfiguracionCampania(ObjetoValor):
    presupuesto: float = 0.0
    moneda: str = "USD"
    canales: List[str] = None
    frecuencia_maxima: int = 3
    duracion_sesion_minutos: int = 30

    def __post_init__(self):
        if self.canales is None:
            object.__setattr__(self, 'canales', ["WEB", "EMAIL"])


@dataclass(frozen=True) 
class MetricasCampania(ObjetoValor):
    impresiones: int = 0
    clics: int = 0
    conversiones: int = 0
    costo_total: float = 0.0
    
    def incrementar_interacciones(self):
        return MetricasCampania(
            impresiones=self.impresiones + 1,
            clics=self.clics,
            conversiones=self.conversiones,
            costo_total=self.costo_total
        )

    def incrementar_clics(self):
        return MetricasCampania(
            impresiones=self.impresiones + 1,
            clics=self.clics + 1,
            conversiones=self.conversiones,
            costo_total=self.costo_total
        )

    def incrementar_conversiones(self, costo_adicional: float = 0.0):
        return MetricasCampania(
            impresiones=self.impresiones,
            clics=self.clics,
            conversiones=self.conversiones + 1,
            costo_total=self.costo_total + costo_adicional
        )

    def calcular_ctr(self) -> float:
        if self.impresiones == 0:
            return 0.0
        return (self.clics / self.impresiones) * 100

    def calcular_cpc(self) -> float:
        if self.clics == 0:
            return 0.0
        return self.costo_total / self.clics
