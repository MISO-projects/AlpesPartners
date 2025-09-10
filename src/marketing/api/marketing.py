# pyright: reportUnreachable=false
import marketing.seedwork.presentacion.api as api
from flask import request, Response
import json
from datetime import datetime
from marketing.seedwork.dominio.excepciones import ExcepcionDominio
from marketing.modulos.campanias.aplicacion.comandos.crear_campania import (
    CrearCampania,
)
from marketing.modulos.campanias.aplicacion.comandos.activar_campania import (
    ActivarCampania,
)
from marketing.modulos.campanias.dominio.repositorios import RepositorioCampania
from marketing.modulos.campanias.infraestructura.fabricas import FabricaRepositorio
from marketing.seedwork.aplicacion.comandos import ejecutar_commando
from marketing.seedwork.aplicacion.queries import ejecutar_query
from marketing.modulos.campanias.aplicacion.queries.obtener_campania import ObtenerCampania
from marketing.modulos.campanias.aplicacion.mapeadores import MapeadorCampaniaDTOJson
from marketing.modulos.campanias.aplicacion.queries.listar_campanias import ListarCampanias
from marketing.modulos.campanias.aplicacion.queries.estadisticas_campanias import EstadisticasCampaniasQuery

bp = api.crear_blueprint("marketing", "/")


@bp.route("/campanias", methods=("POST",))
def crear_campania():
    try:
        data = request.json
        
        required_fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']
        for field in required_fields:
            if field not in data:
                return Response(
                    json.dumps({"error": f"Campo requerido: {field}"}),
                    status=400, mimetype="application/json"
                )
        
        fecha_inicio = datetime.fromisoformat(data['fecha_inicio'].replace('Z', '+00:00'))
        fecha_fin = datetime.fromisoformat(data['fecha_fin'].replace('Z', '+00:00'))
        
        comando = CrearCampania(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo=data.get('tipo', 'DIGITAL'),
            edad_minima=data.get('edad_minima'),
            edad_maxima=data.get('edad_maxima'),
            genero=data.get('genero'),
            ubicacion=data.get('ubicacion'),
            intereses=data.get('intereses', []),
            presupuesto=data.get('presupuesto', 0.0),
            canales=data.get('canales', ['WEB', 'EMAIL'])
        )
        
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
    except Exception as e:
        return Response(
            json.dumps({"error": f"Error interno: {str(e)}"}), 
            status=500, 
            mimetype="application/json"
        )


@bp.route("/campanias/<campania_id>/activar", methods=("PUT",))
def activar_campania(campania_id):
    try:
        comando = ActivarCampania(id_campania=campania_id)
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
    except Exception as e:
        return Response(
            json.dumps({"error": f"Error: {str(e)}"}), 
            status=500, 
            mimetype="application/json"
        )

@bp.route("/campanias/<campania_id>", methods=("GET",))
def obtener_campania(campania_id):
    try:
        query = ObtenerCampania(id=campania_id)
        query_resultado = ejecutar_query(query)
        campania = query_resultado.resultado
        map_campania = MapeadorCampaniaDTOJson()
        response_data = map_campania.dto_a_externo(campania)
        return Response(
            json.dumps(response_data),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"error": f"Error: {str(e)}"}),
            status=500,
            mimetype="application/json"
        )


@bp.route("/campanias", methods=("GET",))
def listar_campanias():
    try:
        query = ListarCampanias(estado=request.args.get('estado'))
        query_resultado = ejecutar_query(query)
        campanias = query_resultado.resultado
        map_campania = MapeadorCampaniaDTOJson()
        response_data = map_campania.lista_dto_a_externo(campanias)
        return Response(
            json.dumps(response_data),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"error": f"Error: {str(e)}"}),
            status=500,
            mimetype="application/json"
        )

@bp.route("/campanias/estadisticas", methods=("GET",))
def estadisticas_campanias():
    try:
        query = EstadisticasCampaniasQuery() 
        query_resultado = ejecutar_query(query)
        return Response(
            json.dumps(query_resultado.resultado),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"error": f"Error: {str(e)}"}),
            status=500,
            mimetype="application/json"
        )
