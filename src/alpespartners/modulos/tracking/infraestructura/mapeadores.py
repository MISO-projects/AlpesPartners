from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.tracking.dominio.entidades import Interaccion
from alpespartners.modulos.tracking.infraestructura.dto import InteraccionDbDto
from datetime import datetime
from uuid import UUID


class MapeadorInteraccionSQLite(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Interaccion.__class__

    def entidad_a_dto(self, entidad: Interaccion) -> InteraccionDbDto:
        return InteraccionDbDto(
            id=str(entidad.id),
            tipo=entidad.tipo,
            marca_temporal=entidad.marca_temporal,
            # identidad_usuario=entidad.identidad_usuario,
            # parametros_tracking=entidad.parametros_tracking,
            # elemento_objetivo=entidad.elemento_objetivo,
            # contexto=entidad.contexto,
            identidad_usuario="temp",
            parametros_tracking="temp",
            elemento_objetivo="temp",
            contexto="temp",
        )

    def dto_a_entidad(self, dto: InteraccionDbDto) -> Interaccion:
        return Interaccion(
            tipo=dto.tipo,
            marca_temporal=dto.marca_temporal,
            identidad_usuario=dto.identidad_usuario,
            parametros_tracking=dto.parametros_tracking,
            elemento_objetivo=dto.elemento_objetivo,
            contexto=dto.contexto,
        )


class MapeadorInteraccionMongoDB(Mapeador):
    def obtener_tipo(self) -> type:
        return Interaccion.__class__

    def entidad_a_dto(self, interaccion: Interaccion) -> dict:
        """Convierte una entidad Interaccion a un documento MongoDB"""
        return {
            "_id": str(interaccion.id),
            "tipo": interaccion.tipo,
            "marca_temporal": interaccion.marca_temporal,
            "identidad_usuario": {
                "id_usuario": interaccion.identidad_usuario.get("id_usuario"),
                "id_anonimo": interaccion.identidad_usuario.get("id_anonimo"),
                "direccion_ip": interaccion.identidad_usuario.get("direccion_ip"),
                "agente_usuario": interaccion.identidad_usuario.get("agente_usuario"),
            },
            "parametros_tracking": {
                "fuente": interaccion.parametros_tracking.get("fuente"),
                "medio": interaccion.parametros_tracking.get("medio"),
                "campania": interaccion.parametros_tracking.get("campaña"),
                "contenido": interaccion.parametros_tracking.get("contenido"),
                "termino": interaccion.parametros_tracking.get("termino"),
                "id_afiliado": interaccion.parametros_tracking.get("id_afiliado", ""),
            },
            "elemento_objetivo": {
                "url": interaccion.elemento_objetivo.get("url"),
                "id_elemento": interaccion.elemento_objetivo.get("id_elemento"),
            },
            "contexto": {
                "url_pagina": interaccion.contexto.get("url_pagina"),
                "url_referente": interaccion.contexto.get("url_referente"),
                "informacion_dispositivo": interaccion.contexto.get(
                    "informacion_dispositivo"
                ),
            },
            "fecha_creacion": datetime.utcnow(),  # Para auditoría
        }

    def dto_a_entidad(self, document: dict) -> Interaccion:
        """Convierte un documento MongoDB a una entidad Interaccion"""
        from alpespartners.modulos.tracking.dominio.objetos_valor import (
            IdentidadUsuario,
            ParametrosTracking,
            ElementoObjetivo,
            ContextoInteraccion,
        )

        identidad_usuario = IdentidadUsuario(
            id_usuario=document["identidad_usuario"].get("id_usuario"),
            id_anonimo=document["identidad_usuario"].get("id_anonimo"),
            direccion_ip=document["identidad_usuario"].get("direccion_ip"),
            agente_usuario=document["identidad_usuario"].get("agente_usuario"),
        )

        parametros_tracking = ParametrosTracking(
            fuente=document["parametros_tracking"].get("fuente"),
            medio=document["parametros_tracking"].get("medio"),
            campania=document["parametros_tracking"].get("campania"),
            contenido=document["parametros_tracking"].get("contenido"),
            termino=document["parametros_tracking"].get("termino"),
            id_afiliado=document["parametros_tracking"].get("id_afiliado"),
        )

        elemento_objetivo = ElementoObjetivo(
            url=document["elemento_objetivo"].get("url"),
            id_elemento=document["elemento_objetivo"].get("id_elemento"),
        )

        contexto = ContextoInteraccion(
            url_pagina=document["contexto"].get("url_pagina"),
            url_referente=document["contexto"].get("url_referente"),
            informacion_dispositivo=document["contexto"].get("informacion_dispositivo"),
        )

        interaccion = Interaccion(
            tipo=document["tipo"],
            marca_temporal=document["marca_temporal"],
            identidad_usuario=identidad_usuario,
            parametros_tracking=parametros_tracking,
            elemento_objetivo=elemento_objetivo,
            contexto=contexto,
        )

        interaccion.id = UUID(document["_id"])

        return interaccion
