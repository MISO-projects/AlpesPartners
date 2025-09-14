
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
from comisiones.modulos.comisiones.aplicacion.queries.listar_comisiones import ListarComisiones, ListarComisionesPorEstado, ListarComisionesPorCampania, ListarComisionesReservadasParaLote
from comisiones.modulos.comisiones.aplicacion.queries.estadisticas_comisiones import ObtenerEstadisticasComisionesPorCampania
from comisiones.seedwork.aplicacion.queries import ejecutar_query
from comisiones.modulos.comisiones.aplicacion.mapeadores import MapeadorComision

bp = api.crear_blueprint("comisiones", "/")


def to_json_safe(obj):
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if hasattr(obj, "__dict__"):
        return {k: to_json_safe(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [to_json_safe(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_json_safe(v) for k, v in obj.items()}
    return obj


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
        
        from comisiones.modulos.comisiones.dominio.entidades import Comision
        from comisiones.modulos.comisiones.dominio.objetos_valor import MontoComision, ConfiguracionComision, TipoComision
        import uuid
        from datetime import datetime
        
        comision_id = uuid.uuid4()
        monto = MontoComision(
            valor=Decimal(str(data['valor_interaccion'])) * Decimal('0.05'),  # 5% de comisión
            moneda=data.get('moneda_interaccion', 'USD')
        )
        
        configuracion = ConfiguracionComision(
            tipo=TipoComision.PORCENTAJE,
            porcentaje=Decimal('5.0')
        )
        
        comision = Comision(
            id=comision_id,
            id_interaccion=str(UUID(data['id_interaccion'])),
            id_campania=str(UUID(data['id_campania'])),
            monto=monto,
            configuracion=configuracion
        )
        
        from comisiones.config.mongo import mongo_config
        comisiones_collection = mongo_config.get_collection("comisiones")
        
        comision_data = {
            "_id": str(comision.id),
            "id_interaccion": str(comision.id_interaccion),
            "id_campania": str(comision.id_campania),
            "monto": {
                "valor": float(comision.monto.valor),
                "moneda": comision.monto.moneda
            },
            "configuracion": {
                "tipo": comision.configuracion.tipo.value,
                "porcentaje": float(comision.configuracion.porcentaje) if comision.configuracion.porcentaje else None
            },
            "estado": "RESERVADA",
            "timestamp": datetime.now().isoformat(),
            "tipo_interaccion": data['tipo_interaccion'],
            "fraud_ok": data.get('fraud_ok', True),
            "score_fraude": data.get('score_fraude', 0)
        }
        
        comisiones_collection.insert_one(comision_data)
        
        print(f"Comisión {comision.id} creada exitosamente para interacción {data['id_interaccion']}")
        
        return Response(
            json.dumps({
                "mensaje": "Comisión reservada exitosamente",
                "id_comision": str(comision.id),
                "monto": float(comision.monto.valor),
                "moneda": comision.monto.moneda
            }), 
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


@bp.route("/comisiones/<comision_id>", methods=("GET",))
def obtener_comision(comision_id):
    try:
        query = ObtenerComision(id=UUID(comision_id))
        query_resultado = ejecutar_query(query)
        comision = query_resultado.resultado
        map_comision = MapeadorComision()
        comision_dto = map_comision.entidad_a_dto(comision)
        return Response(
            json.dumps(to_json_safe(comision_dto)),
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
        from comisiones.config.mongo import mongo_config
        comisiones_collection = mongo_config.get_collection("comisiones")
        
        estado = request.args.get('estado')
        id_campania = request.args.get('id_campania')
        limite = int(request.args.get('limite', 100))
        
        filtro = {}
        if estado:
            filtro['estado'] = estado
        if id_campania:
            filtro['id_campania'] = id_campania
            
        cursor = comisiones_collection.find(filtro).limit(limite)
        comisiones = list(cursor)
        
        for comision in comisiones:
            if '_id' in comision:
                comision['id'] = comision.pop('_id')
        
        return Response(
            json.dumps(to_json_safe(comisiones)),
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
        id_campania = request.args.get('id_campania')
        if id_campania:
            from uuid import UUID
            query = ObtenerEstadisticasComisionesPorCampania(id_campania=UUID(id_campania))
        else:
            from comisiones.modulos.comisiones.aplicacion.queries.estadisticas_comisiones import ObtenerEstadisticasComisiones
            query = ObtenerEstadisticasComisiones() 
        query_resultado = ejecutar_query(query)
        return Response(
            json.dumps(to_json_safe(query_resultado.resultado)),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"error": f"Error: {str(e)}"}),
            status=500,
            mimetype="application/json"
        )
