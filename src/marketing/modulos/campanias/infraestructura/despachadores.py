import pulsar
from pulsar.schema import AvroSchema
from marketing.modulos.campanias.infraestructura.schema.v1.eventos import (
    EventoCampaniaCreada,
    EventoCampaniaActivada,
    EventoCampaniaDesactivada,
    EventoInteraccionRecibida,
    CampaniaCreadaPayload,
    CampaniaActivadaPayload,
    CampaniaDesactivadaPayload,
    InteraccionRecibidaPayload
)
from marketing.modulos.campanias.infraestructura.schema.v1.comandos import (
    ComandoCrearCampania,
    ComandoActivarCampania,
    CrearCampaniaPayload,
    ActivarCampaniaPayload
)
from marketing.seedwork.infraestructura import utils


class DespachadorMarketing:
    def __init__(self):
        self.cliente = None
        
    def _obtener_cliente(self):
        if not self.cliente:
            self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        return self.cliente
    
    def _publicar_mensaje(self, mensaje, topico, schema_class):
        cliente = self._obtener_cliente()
        try:
            import json
            # Usar JSON simple en lugar de AVRO para evitar problemas de schema
            publicador = cliente.create_producer(topico)

            # Convertir el mensaje a JSON
            if hasattr(mensaje, '__dict__'):
                mensaje_dict = mensaje.__dict__
            else:
                mensaje_dict = mensaje

            mensaje_json = json.dumps(mensaje_dict, default=str).encode('utf-8')
            publicador.send(mensaje_json)
            print(f'✓ Evento Marketing publicado en tópico: {topico}')
        except Exception as e:
            print(f'✗ Error publicando evento Marketing: {e}')
            raise e
        finally:
            if cliente:
                cliente.close()

    def publicar_campania_creada(self, evento):
        payload = CampaniaCreadaPayload(
            id_campania=str(evento.id_campania),
            nombre=evento.nombre,
            tipo=evento.tipo,
            fecha_inicio=int(evento.fecha_inicio.timestamp() * 1000),
            fecha_fin=int(evento.fecha_fin.timestamp() * 1000),
            segmento={
                'edad_minima': evento.segmento.edad_minima,
                'edad_maxima': evento.segmento.edad_maxima,
                'genero': evento.segmento.genero,
                'ubicacion': evento.segmento.ubicacion,
                'intereses': evento.segmento.intereses or []
            }
        )
        evento_integracion = EventoCampaniaCreada(data=payload)
        self._publicar_mensaje(
            evento_integracion, 
            "campania-creada", 
            EventoCampaniaCreada
        )

    def publicar_campania_activada(self, evento):
        payload = CampaniaActivadaPayload(
            id_campania=str(evento.id_campania),
            nombre=evento.nombre,
            fecha_activacion=int(evento.fecha_activacion.timestamp() * 1000)
        )
        evento_integracion = EventoCampaniaActivada(data=payload)
        self._publicar_mensaje(
            evento_integracion,
            "campania-activada",
            EventoCampaniaActivada
        )

    def publicar_campania_desactivada(self, evento):
        payload = CampaniaDesactivadaPayload(
            id_campania=str(evento.id_campania),
            razon=evento.razon,
            fecha_desactivacion=int(evento.fecha_evento.timestamp() * 1000)
        )
        evento_integracion = EventoCampaniaDesactivada(data=payload)
        self._publicar_mensaje(
            evento_integracion,
            "campania-desactivada",
            EventoCampaniaDesactivada
        )

    def publicar_interaccion_recibida(self, evento):
        payload = InteraccionRecibidaPayload(
            id_campania=str(evento.id_campania),
            tipo_interaccion=evento.tipo_interaccion,
            parametros_tracking=evento.parametros_tracking or {},
            timestamp=int(evento.timestamp.timestamp() * 1000)
        )
        evento_integracion = EventoInteraccionRecibida(data=payload)
        self._publicar_mensaje(
            evento_integracion,
            "marketing-interaccion-procesada",
            EventoInteraccionRecibida
        )

    def publicar_comando_crear_campania(self, comando):
        payload = CrearCampaniaPayload(
            nombre=comando.nombre,
            descripcion=comando.descripcion,
            fecha_inicio=int(comando.fecha_inicio.timestamp() * 1000),
            fecha_fin=int(comando.fecha_fin.timestamp() * 1000),
            tipo=comando.tipo,
            segmento={},
            configuracion={}
        )
        comando_integracion = ComandoCrearCampania(data=payload)
        self._publicar_mensaje(
            comando_integracion,
            "crear-campania-comando",
            ComandoCrearCampania
        )
