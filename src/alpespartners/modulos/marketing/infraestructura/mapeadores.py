from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.marketing.dominio.entidades import Campania, EstadoCampania
from alpespartners.modulos.marketing.dominio.objetos_valor import (
    SegmentoAudiencia,
    ConfiguracionCampania, 
    MetricasCampania
)
from alpespartners.modulos.marketing.infraestructura.dto import CampaniaDbDto
import json
import uuid


class MapeadorCampania(Mapeador):
    
    def obtener_tipo(self) -> type:
        return Campania.__class__

    def entidad_a_dto(self, entidad: Campania) -> CampaniaDbDto:
        segmento_json = {
            'edad_minima': entidad.segmento.edad_minima,
            'edad_maxima': entidad.segmento.edad_maxima,
            'genero': entidad.segmento.genero,
            'ubicacion': entidad.segmento.ubicacion,
            'intereses': entidad.segmento.intereses or []
        }
        
        configuracion_json = {
            'presupuesto': entidad.configuracion.presupuesto,
            'moneda': entidad.configuracion.moneda,
            'canales': entidad.configuracion.canales or [],
            'frecuencia_maxima': entidad.configuracion.frecuencia_maxima,
            'duracion_sesion_minutos': entidad.configuracion.duracion_sesion_minutos
        }
        
        metricas_json = {
            'impresiones': entidad.metricas.impresiones,
            'clics': entidad.metricas.clics,
            'conversiones': entidad.metricas.conversiones,
            'costo_total': entidad.metricas.costo_total
        }
        
        return CampaniaDbDto(
            id=str(entidad.id),
            nombre=entidad.nombre,
            descripcion=entidad.descripcion,
            fecha_inicio=entidad.fecha_inicio,
            fecha_fin=entidad.fecha_fin,
            estado=entidad.estado.value,
            tipo=entidad.tipo,
            segmento=segmento_json,
            configuracion=configuracion_json,
            metricas=metricas_json,
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion
        )

    def dto_a_entidad(self, dto: CampaniaDbDto) -> Campania:
        segmento_dict = dto.segmento or {}
        segmento = SegmentoAudiencia(
            edad_minima=segmento_dict.get('edad_minima'),
            edad_maxima=segmento_dict.get('edad_maxima'),
            genero=segmento_dict.get('genero'),
            ubicacion=segmento_dict.get('ubicacion'),
            intereses=segmento_dict.get('intereses', [])
        )
        
        configuracion_dict = dto.configuracion or {}
        configuracion = ConfiguracionCampania(
            presupuesto=configuracion_dict.get('presupuesto', 0.0),
            moneda=configuracion_dict.get('moneda', 'USD'),
            canales=configuracion_dict.get('canales', []),
            frecuencia_maxima=configuracion_dict.get('frecuencia_maxima', 3),
            duracion_sesion_minutos=configuracion_dict.get('duracion_sesion_minutos', 30)
        )
        
        metricas_dict = dto.metricas or {}
        metricas = MetricasCampania(
            impresiones=metricas_dict.get('impresiones', 0),
            clics=metricas_dict.get('clics', 0),
            conversiones=metricas_dict.get('conversiones', 0),
            costo_total=metricas_dict.get('costo_total', 0.0)
        )
        
        return Campania(
            id=uuid.UUID(dto.id),
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            estado=EstadoCampania(dto.estado),
            tipo=dto.tipo,
            segmento=segmento,
            configuracion=configuracion,
            metricas=metricas,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion
        )
