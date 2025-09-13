from atribucion.seedwork.dominio.excepciones import ExcepcionDominio
from atribucion.modulos.atribucion.aplicacion.mapeadores import MapeadorAtribucionDTOJson
import atribucion.seedwork.presentacion.api as api
from atribucion.modulos.atribucion.aplicacion.comandos.registrar_atribucion import RegistrarAtribucion
from atribucion.seedwork.aplicacion.comandos import ejecutar_commando
import json
from flask import request, Response
 
bp = api.crear_blueprint("atribucion", "/")
 
@bp.route("/atribucion-registrada-comando", methods=("POST",))
def atribucion_registrada_asincrona():
    try:
        atribucion_dict = request.json
        map_atribucion = MapeadorAtribucionDTOJson() 
        atribucion_dto = map_atribucion.externo_a_dto(atribucion_dict)

        comando = RegistrarAtribucion(atribucion=atribucion_dto)
        print(f"API: Comando '{type(comando).__name__}' creado. Despachando...")
        ejecutar_commando(comando)
        return Response(
            json.dumps({}), 
            status=202, 
            mimetype="application/json"
        )

        
    except ExcepcionDominio as e:
        return Response(
            json.dumps({"error": str(e)}), 
            status=400, 
            mimetype="application/json"
        )