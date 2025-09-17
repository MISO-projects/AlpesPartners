from atribucion.seedwork.dominio.excepciones import ExcepcionDominio
from atribucion.modulos.atribucion.aplicacion.mapeadores import MapeadorAtribucionDTOJson
import atribucion.seedwork.presentacion.api as api
from atribucion.modulos.atribucion.aplicacion.comandos.registrar_atribucion import RegistrarAtribucion
from atribucion.modulos.atribucion.aplicacion.comandos.revertir_atribucion import RevertirAtribucion
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

        comando = RegistrarAtribucion(
            atribucion_dto=atribucion_dto,
            datos_evento_dict=atribucion_dict
        )
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
    

@bp.route("/revertir-atribucion/<string:journey_id>", methods=("POST",))
def revertir_atribucion_comando(journey_id: str):
    """
    Endpoint de prueba para ejecutar el comando 'RevertirAtribucion'.
    """
    try:
        print(f"API: Recibida petición en /revertir-atribucion para el ID: {journey_id}")
        comando = RevertirAtribucion(journey_id=journey_id)
        ejecutar_commando(comando)
        
        return Response('{"mensaje": "Comando de reversión aceptado"}', status=202, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
