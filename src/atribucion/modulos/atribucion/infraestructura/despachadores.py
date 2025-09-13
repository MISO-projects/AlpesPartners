import pulsar
from pulsar.schema import AvroSchema, Record
import json
from .schema.v1.eventos import EventoConversionAtribuida, ConversionAtribuidaPayload, MontoSchema
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

    def publicar_evento_conversion_atribuida(self, resultado_atribucion: list, datos_evento_original: dict, topico='eventos-atribucion'):
        
        if not resultado_atribucion:
            print("DESPACHADOR: No hay atribución calculada para publicar.")
            return
            
        atribucion_principal = resultado_atribucion[0]
        
        print(f"DESPACHADOR: Mapeando resultado de atribución a Payload: {atribucion_principal}")
        
        payload = ConversionAtribuidaPayload(
            id_interaccion_atribuida=str(uuid.uuid4()),
            id_campania=str(atribucion_principal.touchpoint.campania_id),
            tipo_conversion=datos_evento_original.get('tipo', 'UNKNOWN'),
            monto_atribuido=MontoSchema(
                valor=float(atribucion_principal.valor_atribuido),
                moneda='USD'
            ),
            id_interaccion_original=datos_evento_original.get('id_interaccion'),
            score_fraude=15 # TODO: Calcular un score de fraude real
        )
        
        evento_integracion = EventoConversionAtribuida(data=payload)
        print(f"DESPACHADOR: Evento mapeado: {evento_integracion}")
        self._publicar_mensaje(evento_integracion, topico, EventoConversionAtribuida)