from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from alpespartners.seedwork.dominio.entidades import AgregacionRaiz
from alpespartners.modulos.marketing.dominio.objetos_valor import (
    SegmentoAudiencia, 
    ConfiguracionCampania,
    MetricasCampania
)
from alpespartners.modulos.marketing.dominio.eventos import (
    CampaniaCreada,
    CampaniaActivada,
    CampaniaDesactivada,
    InteraccionRecibida
)


class EstadoCampania(Enum):
    BORRADOR = "BORRADOR"
    ACTIVA = "ACTIVA" 
    PAUSADA = "PAUSADA"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"


@dataclass
class Campania(AgregacionRaiz):
    nombre: str = field(default="")
    descripcion: str = field(default="")
    fecha_inicio: datetime = field(default_factory=datetime.now)
    fecha_fin: datetime = field(default_factory=datetime.now)
    estado: EstadoCampania = field(default=EstadoCampania.BORRADOR)
    tipo: str = field(default="DIGITAL")
    segmento: SegmentoAudiencia = field(default_factory=SegmentoAudiencia)
    configuracion: ConfiguracionCampania = field(default_factory=ConfiguracionCampania)
    metricas: MetricasCampania = field(default_factory=MetricasCampania)

    def crear_campania(self):
        if not self.nombre or not self.descripcion:
            raise ValueError("Nombre y descripción son requeridos")
        
        self.agregar_evento(
            CampaniaCreada(
                id_campania=self.id,
                nombre=self.nombre,
                tipo=self.tipo,
                fecha_inicio=self.fecha_inicio,
                fecha_fin=self.fecha_fin,
                segmento=self.segmento
            )
        )

    def activar_campania(self):
        if self.estado != EstadoCampania.BORRADOR:
            raise ValueError("Solo se pueden activar campañas en borrador")
        
        self.estado = EstadoCampania.ACTIVA
        self.agregar_evento(
            CampaniaActivada(
                id_campania=self.id,
                nombre=self.nombre,
                fecha_activacion=datetime.now()
            )
        )

    def procesar_interaccion(self, evento_tracking):
        nuevas_metricas = self.metricas.incrementar_interacciones()
        self.metricas = nuevas_metricas
        
        self.agregar_evento(
            InteraccionRecibida(
                id_campania=self.id,
                tipo_interaccion=evento_tracking.tipo,
                parametros_tracking=evento_tracking.parametros_tracking,
                timestamp=evento_tracking.marca_temporal
            )
        )

    def desactivar_campania(self, razon: str = None):
        if self.estado != EstadoCampania.ACTIVA:
            raise ValueError("Solo se pueden desactivar campañas activas")
        
        self.estado = EstadoCampania.PAUSADA
        self.agregar_evento(
            CampaniaDesactivada(
                id_campania=self.id,
                razon=razon or "Desactivada manualmente"
            )
        )
