import alpespartners.seedwork.presentacion.api as api
from flask import request, Response
import json
from datetime import datetime
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio
from alpespartners.modulos.marketing.aplicacion.comandos.crear_campania import (
    CrearCampania,
    CrearCampaniaHandler
)
from alpespartners.modulos.marketing.aplicacion.comandos.activar_campania import (
    ActivarCampania,
    ActivarCampaniaHandler
)
from alpespartners.modulos.marketing.dominio.repositorios import RepositorioCampania
from alpespartners.modulos.marketing.infraestructura.fabricas import FabricaRepositorio

bp = api.crear_blueprint("marketing", "/marketing")


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
        
        handler = CrearCampaniaHandler()
        campania = handler.handle(comando)
        
        response_data = {
            "id": str(campania.id),
            "nombre": campania.nombre,
            "descripcion": campania.descripcion,
            "estado": campania.estado.value,
            "fecha_inicio": campania.fecha_inicio.isoformat(),
            "fecha_fin": campania.fecha_fin.isoformat(),
            "tipo": campania.tipo,
            "metricas": {
                "impresiones": campania.metricas.impresiones,
                "clics": campania.metricas.clics,
                "conversiones": campania.metricas.conversiones,
                "costo_total": campania.metricas.costo_total
            },
            "message": "Campaña creada exitosamente"
        }
        
        return Response(
            json.dumps(response_data, default=str), 
            status=201, 
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
        handler = ActivarCampaniaHandler()
        campania = handler.handle(comando)
        
        response_data = {
            "id": str(campania.id),
            "nombre": campania.nombre,
            "estado": campania.estado.value,
            "message": "Campaña activada exitosamente"
        }
        
        return Response(
            json.dumps(response_data), 
            status=200, 
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
        fabrica_repo = FabricaRepositorio()
        repositorio = fabrica_repo.crear_objeto(RepositorioCampania)
        
        import uuid
        campania = repositorio.obtener_por_id(uuid.UUID(campania_id))
        
        if not campania:
            return Response(
                json.dumps({"error": "Campaña no encontrada"}),
                status=404,
                mimetype="application/json"
            )
        
        response_data = {
            "id": str(campania.id),
            "nombre": campania.nombre,
            "descripcion": campania.descripcion,
            "estado": campania.estado.value,
            "fecha_inicio": campania.fecha_inicio.isoformat(),
            "fecha_fin": campania.fecha_fin.isoformat(),
            "tipo": campania.tipo,
            "segmento": {
                "edad_minima": campania.segmento.edad_minima,
                "edad_maxima": campania.segmento.edad_maxima,
                "genero": campania.segmento.genero,
                "ubicacion": campania.segmento.ubicacion,
                "intereses": campania.segmento.intereses
            },
            "configuracion": {
                "presupuesto": campania.configuracion.presupuesto,
                "moneda": campania.configuracion.moneda,
                "canales": campania.configuracion.canales,
                "frecuencia_maxima": campania.configuracion.frecuencia_maxima
            },
            "metricas": {
                "impresiones": campania.metricas.impresiones,
                "clics": campania.metricas.clics,
                "conversiones": campania.metricas.conversiones,
                "costo_total": campania.metricas.costo_total,
                "ctr": campania.metricas.calcular_ctr(),
                "cpc": campania.metricas.calcular_cpc()
            }
        }
        
        return Response(
            json.dumps(response_data, default=str),
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
        fabrica_repo = FabricaRepositorio()
        repositorio = fabrica_repo.crear_objeto(RepositorioCampania)
        
        estado_filtro = request.args.get('estado') 
        
        if estado_filtro == 'ACTIVA':
            campanias = repositorio.obtener_activas()
        else:
            campanias = repositorio.obtener_todos()
        
        response_data = {
            "campanias": [],
            "total": len(campanias)
        }
        
        for campania in campanias:
            campania_data = {
                "id": str(campania.id),
                "nombre": campania.nombre,
                "descripcion": campania.descripcion,
                "estado": campania.estado.value,
                "fecha_inicio": campania.fecha_inicio.isoformat(),
                "fecha_fin": campania.fecha_fin.isoformat(),
                "tipo": campania.tipo,
                "metricas": {
                    "impresiones": campania.metricas.impresiones,
                    "clics": campania.metricas.clics,
                    "conversiones": campania.metricas.conversiones,
                    "ctr": campania.metricas.calcular_ctr()
                }
            }
            response_data["campanias"].append(campania_data)
        
        return Response(
            json.dumps(response_data, default=str),
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
        fabrica_repo = FabricaRepositorio()
        repositorio = fabrica_repo.crear_objeto(RepositorioCampania)
        
        todas_campanias = repositorio.obtener_todos()
        campanias_activas = repositorio.obtener_activas()
        
        total_impresiones = sum(c.metricas.impresiones for c in todas_campanias)
        total_clics = sum(c.metricas.clics for c in todas_campanias)
        total_conversiones = sum(c.metricas.conversiones for c in todas_campanias)
        costo_total = sum(c.metricas.costo_total for c in todas_campanias)
        
        ctr_promedio = (total_clics / total_impresiones * 100) if total_impresiones > 0 else 0
        cpc_promedio = (costo_total / total_clics) if total_clics > 0 else 0
        
        response_data = {
            "resumen": {
                "total_campanias": len(todas_campanias),
                "campanias_activas": len(campanias_activas),
                "total_impresiones": total_impresiones,
                "total_clics": total_clics,
                "total_conversiones": total_conversiones,
                "costo_total": costo_total,
                "ctr_promedio": round(ctr_promedio, 2),
                "cpc_promedio": round(cpc_promedio, 2)
            }
        }
        
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
