import pulsar
from pulsar.schema import AvroSchema, Record
import json
from .schema.v1.eventos import EventoConversionAtribuida, ConversionAtribuidaPayload, MontoSchema
from atribucion.modulos.atribucion.dominio.entidades import Journey
from atribucion.seedwork.infraestructura import utils
import uuid


def avro_to_dict(record) -> dict:
    """Convierte un objeto Avro Record a un diccionario de Python recursivamente."""
    if not isinstance(record, Record):
        return record
    
    result = {}
    for key, value in record.__dict__.items():
        if key.startswith('_'):
            continue
        if isinstance(value, Record):
            result[key] = avro_to_dict(value)
        elif isinstance(value, list):
            result[key] = [avro_to_dict(item) for item in value]
        else:
            result[key] = value
    return result

def calcular_score_fraude_basico(resultado_atribucion: list) -> int:
    """Calcula un score de fraude básico usando los datos de atribución"""
    if not resultado_atribucion:
        return 0
        
    score = 0
    atribucion_principal = resultado_atribucion[0]
    touchpoint = atribucion_principal.touchpoint
    
    # Factor 1: Campaña vacía o None (sospechoso)
    if not touchpoint.campania_id:
        score += 25
    
    # Factor 2: Canal sospechoso
    if touchpoint.canal in ['unknown', 'bot', 'crawler']:
        score += 60
    
    # Factor 3: Tipo de interacción de bajo valor
    # if touchpoint.tipo_interaccion in ['IMPRESSION', 'VIEW']:
    #     score += 10
    
    # Factor 4: Valor atribuido muy bajo o 0
    # if atribucion_principal.valor_atribuido <= 0:
    #     score += 20
    
    score_final = min(score, 100)
    return score_final

class DespachadorEventosAtribucion:
    def _publicar_mensaje(self, mensaje, topico, schema_class):
        try:
            print("DESPACHADOR: Conectando al broker Pulsar...")
            cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
            print("DESPACHADOR: Conexión establecida.")
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema_class))
            
            print(f"DESPACHADOR: Publicando mensaje en tópico: {topico}")
            publicador.send(mensaje)
            
            mensaje_completo = avro_to_dict(mensaje.data)
            print("DESPACHADOR: Mensaje publicado exitosamente:")
            print(json.dumps(mensaje_completo, indent=2, default=str, ensure_ascii=False))
            
            cliente.close()
        except Exception as e:
            print(f"ERROR DESPACHADOR: No se pudo publicar el evento. Causa: {e}")

    def publicar_evento_conversion_atribuida(self,journey: Journey, resultado_atribucion: list, datos_evento_original: dict,  topico='eventos-atribucion'):
        
        if not resultado_atribucion:
            print("DESPACHADOR: No hay atribución calculada para publicar.")
            return
            
        atribucion_principal = resultado_atribucion[0]
        payload = ConversionAtribuidaPayload(
            id_interaccion_atribuida=str(journey.id),
            id_campania=str(atribucion_principal.touchpoint.campania_id),
            id_afiliado=str(atribucion_principal.touchpoint.afiliado_id),
            tipo_conversion=datos_evento_original.get('tipo', 'UNKNOWN'),
            monto_atribuido=MontoSchema(
                valor=float(atribucion_principal.valor_atribuido),
                moneda='USD'
            ),
            id_interaccion_original=datos_evento_original.get('id_interaccion', 'UNKNOWN'),
            score_fraude=calcular_score_fraude_basico(resultado_atribucion)
        )
        
        evento_integracion = EventoConversionAtribuida(data=payload)
        self._publicar_mensaje(evento_integracion, topico, EventoConversionAtribuida)