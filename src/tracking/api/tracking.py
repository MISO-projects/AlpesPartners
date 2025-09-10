# pyright: reportUnreachable=false
import tracking.seedwork.presentacion.api as api
from flask import request, Response
import json
from tracking.seedwork.dominio.excepciones import ExcepcionDominio
from tracking.modulos.interacciones.aplicacion.mapeadores import (
    MapeadorInteraccionDTOJson,
)
from tracking.modulos.interacciones.aplicacion.comandos.registrar_interaccion import (
    RegistrarInteraccion,
)
from tracking.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint("tracking", "/")


@bp.route("/interaccion", methods=("POST",))
def registrar_interaccion():
    try:
        interaccion_dict = request.json
        map_interaccion = MapeadorInteraccionDTOJson()
        interaccion_dto = map_interaccion.externo_a_dto(interaccion_dict)
        comando = RegistrarInteraccion(
            tipo=interaccion_dto.tipo,
            marca_temporal=interaccion_dto.marca_temporal,
            identidad_usuario=interaccion_dto.identidad_usuario,
            parametros_tracking=interaccion_dto.parametros_tracking,
            elemento_objetivo=interaccion_dto.elemento_objetivo,
            contexto=interaccion_dto.contexto,
        )
        ejecutar_commando(comando)
        return Response('{}', status=202, mimetype="application/json")
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )
