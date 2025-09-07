from alpespartners.seedwork.aplicacion.dto import Mapeador as AppMap
from alpespartners.modulos.marketing.aplicacion.dto import CampaniaDTO
from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.marketing.dominio.entidades import Campania


class MapeadorCampaniaDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> CampaniaDTO:
        return CampaniaDTO(
            id=externo["id"],
            nombre=externo["nombre"],
            descripcion=externo["descripcion"],
            fecha_inicio=externo["fecha_inicio"],
            fecha_fin=externo["fecha_fin"],
            estado=externo["estado"],
            tipo=externo["tipo"],
            segmento=externo["segmento"],
            configuracion=externo["configuracion"],
            metricas=externo["metricas"],
        )

    def dto_a_externo(self, dto: CampaniaDTO) -> dict:
        return {
            "id": str(dto.id),
            "nombre": dto.nombre,
            "descripcion": dto.descripcion,
            "estado": dto.estado.value,
            "fecha_inicio": dto.fecha_inicio.isoformat(),
            "fecha_fin": dto.fecha_fin.isoformat(),
            "tipo": dto.tipo,
            "segmento": {
                "edad_minima": dto.segmento.edad_minima,
                "edad_maxima": dto.segmento.edad_maxima,
                "genero": dto.segmento.genero,
                "ubicacion": dto.segmento.ubicacion,
                "intereses": dto.segmento.intereses,
            },
            "configuracion": {
                "presupuesto": dto.configuracion.presupuesto,
                "moneda": dto.configuracion.moneda,
                "canales": dto.configuracion.canales,
                "frecuencia_maxima": dto.configuracion.frecuencia_maxima,
            },
            "metricas": {
                "impresiones": dto.metricas.impresiones,
                "clics": dto.metricas.clics,
                "conversiones": dto.metricas.conversiones,
                "costo_total": dto.metricas.costo_total,
                "ctr": dto.metricas.calcular_ctr(),
                "cpc": dto.metricas.calcular_cpc(),
            },
        }

    def dto_a_externo_simple(self, dto: CampaniaDTO) -> dict:
        """Convierte CampaniaDTO a formato externo simplificado para listas"""
        return {
            "id": str(dto.id),
            "nombre": dto.nombre,
            "descripcion": dto.descripcion,
            "estado": dto.estado.value,
            "fecha_inicio": dto.fecha_inicio.isoformat(),
            "fecha_fin": dto.fecha_fin.isoformat(),
            "tipo": dto.tipo,
            "metricas": {
                "impresiones": dto.metricas.impresiones,
                "clics": dto.metricas.clics,
                "conversiones": dto.metricas.conversiones,
                "ctr": dto.metricas.calcular_ctr()
            }
        }
    
    def lista_dto_a_externo(self, campanias: list[CampaniaDTO]) -> dict:
        """Convierte lista de CampaniaDTO a formato externo con estructura de lista"""
        return {
            "campanias": [self.dto_a_externo_simple(campania) for campania in campanias],
            "total": len(campanias)
        }


class MapeadorCampania(Mapeador):
    def obtener_tipo(self) -> type:
        return Campania.__class__

    def entidad_a_dto(self, entidad: Campania) -> CampaniaDTO:
        return CampaniaDTO(
            id=entidad.id,
            nombre=entidad.nombre,
            descripcion=entidad.descripcion,
            fecha_inicio=entidad.fecha_inicio,
            fecha_fin=entidad.fecha_fin,
            estado=entidad.estado,
            tipo=entidad.tipo,
            segmento=entidad.segmento,
            configuracion=entidad.configuracion,
            metricas=entidad.metricas,
        )

    def dto_a_entidad(self, dto: CampaniaDTO) -> Campania:
        return Campania(
            id=dto.id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            estado=dto.estado,
            tipo=dto.tipo,
            segmento=dto.segmento,
            configuracion=dto.configuracion,
            metricas=dto.metricas,
        )
