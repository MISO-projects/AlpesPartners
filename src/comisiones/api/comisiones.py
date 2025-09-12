
# pyright: reportUnreachable=false
import comisiones.seedwork.presentacion.api as api
from flask import request, Response
import json
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from comisiones.seedwork.dominio.excepciones import ExcepcionDominio
from comisiones.modulos.comisiones.aplicacion.comandos.reservar_comision import ReservarComision
from comisiones.modulos.comisiones.aplicacion.comandos.confirmar_comision import ConfirmarComision, ConfirmarComisionesEnLote
from comisiones.modulos.comisiones.aplicacion.comandos.revertir_comision import RevertirComision
from comisiones.seedwork.aplicacion.comandos import ejecutar_commando
from comisiones.modulos.comisiones.aplicacion.queries.obtener_comision import ObtenerComision
from comisiones.modulos.comisiones.aplicacion.queries.listar_comisiones import ListarComisiones
from comisiones.modulos.comisiones.aplicacion.queries.estadisticas_comisiones import EstadisticasComisionesQuery
from comisiones.seedwork.aplicacion.queries import ejecutar_query
from comisiones.modulos.comisiones.aplicacion.mapeadores import MapeadorComisionDTOJson

bp = api.crear_blueprint("comisiones", "/")

@bp.route("/comisiones", methods=("POST",))
def reservar_comision():
    try:
        data = request.json
        
        required_fields = ['id_interaccion', 'id_campania', 'tipo_interaccion', 'valor_interaccion']
        for field in required_fields:
            if field not in data:
                return Response(
                    json.dumps({"error": f"Campo requerido: {field}"}),
                    status=400, mimetype="application/json"
                )
        
        comando = ReservarComision(
            id_interaccion=UUID(data['id_interaccion']),
            id_campania=UUID(data['id_campania']),
            tipo_interaccion=data['tipo_interaccion'],
            valor_interaccion=Decimal(str(data['valor_interaccion'])),
            moneda_interaccion=data.get('moneda_interaccion', 'USD'),
            fraud_ok=data.get('fraud_ok', True),
            score_fraude=data.get('score_fraude', 0),
            parametros_adicionales=data.get('parametros_adicionales', {})
        )
        
        ejecutar_commando(comando)
        return Response(
            json.dumps({"mensaje": "Comisión reservada exitosamente"}), 
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

@bp.route("/comisiones/<comision_id>/confirmar", methods=("PUT",))
def confirmar_comision(comision_id):
    try:
        data = request.json or {}
        
        comando = ConfirmarComision(
            id_comision=UUID(comision_id),
            lote_confirmacion=data.get('lote_confirmacion', ''),
            referencia_pago=data.get('referencia_pago', '')
        )
        
        ejecutar_commando(comando)
        return Response(
            json.dumps({"mensaje": "Comisión confirmada exitosamente"}), 
            status=202, 
            mimetype="application/json"
        )
        
    except ValueError as e:
        return Response(
            json.dumps({"error": str(e)}), 
            status=404, 
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

@bp.route("/comisiones/confirmar-lote", methods=("POST",))
def confirmar_comisiones_lote():
    try:
        data = request.json or {}
        
        comando = ConfirmarComisionesEnLote(
            limite_comisiones=data.get('limite_comisiones', 100),
            lote_id=data.get('lote_id')
        )
        
        ejecutar_commando(comando)
        return Response(
            json.dumps({"mensaje": "Lote de comisiones confirmado exitosamente"}), 
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

@bp.route("/comisiones/<comision_id>/revertir", methods=("PUT",))
def revertir_comision(comision_id):
    try:
        data = request.json
        
        if not data or 'motivo' not in data:
            return Response(
                json.dumps({"error": "Campo requerido: motivo"}),
                status=400, mimetype="application/json"
            )
        
        comando = RevertirComision(
            id_comision=UUID(comision_id),
            motivo=data['motivo']
        )
        
        ejecutar_commando(comando)
        return Response(
            json.dumps({"mensaje": "Comisión revertida exitosamente"}), 
            status=202, 
            mimetype="application/json"
        )
        
    except ValueError as e:
        return Response(
            json.dumps({"error": str(e)}), 
            status=404, 
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

@bp.route("/comisiones/<comision_id>", methods=("GET",))
def obtener_comision(comision_id):
    try:
        query = ObtenerComision(id=UUID(comision_id))
        query_resultado = ejecutar_query(query)
        comision = query_resultado.resultado
        map_comision = MapeadorComisionDTOJson()
        response_data = map_comision.dto_a_externo(comision)
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

@bp.route("/comisiones", methods=("GET",))
def listar_comisiones():
    try:
        query = ListarComisiones(
            estado=request.args.get('estado'),
            id_campania=request.args.get('id_campania'),
            para_lote=request.args.get('para_lote', 'false').lower() == 'true',
            limite=int(request.args.get('limite', 100))
        )
        query_resultado = ejecutar_query(query)
        comisiones = query_resultado.resultado
        map_comision = MapeadorComisionDTOJson()
        response_data = map_comision.lista_dto_a_externo(comisiones)
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

@bp.route("/comisiones/estadisticas", methods=("GET",))
def estadisticas_comisiones():
    try:
        query = EstadisticasComisionesQuery(
            id_campania=request.args.get('id_campania')
        ) 
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
