import pulsar
from pulsar.schema import AvroSchema
from atribucion.modulos.atribucion.infraestructura.schema.v1.eventos import (
    EventoInteraccionAtribuidaRecibida,
    InteraccionAtribuidaRecibidaPayload,
)
from atribucion.seedwork.infraestructura import utils


class DespachadorAtribucion:
    def _publicar_mensaje(self, mensaje, topico, schema_class):
        print(f' AQUI ESTA DISPARANDO ATRIBUCION')
        print(mensaje)
        print(topico)
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        try:
            publicador = cliente.create_producer(
                topico, schema=AvroSchema(schema_class)
            )
            publicador.send(mensaje)
            print(f' Mensaje Atribucion publicado en tópico: {topico}')
        except Exception as e:
            print(f' Error publicando mensaje Atribucion: {e}')
            print(f' [FALLBACK] Publicando mensaje {mensaje.data} en tópico {topico}')
        finally:
            if cliente:
                cliente.close()

    def publicar_interaccion_atribuida(self, evento, topico="interaccion-atribuida"):
        from atribucion.modulos.atribucion.infraestructura.schema.v1.eventos import MontoComisionSchema
        
        # Convertir MontoComision (dominio) a MontoComisionSchema (Pulsar)
        monto_schema = MontoComisionSchema(
            valor=float(evento.valor_interaccion.valor),
            moneda=evento.valor_interaccion.moneda
        )
        
        payload = InteraccionAtribuidaRecibidaPayload(
            id_interaccion=str(evento.id_interaccion),
            id_campania=str(evento.id_campania),
            tipo_interaccion=evento.tipo_interaccion,
            valor_interaccion=monto_schema,
            fraud_ok=evento.fraud_ok,
            score_fraude=evento.score_fraude,
            timestamp=int(evento.timestamp.timestamp() * 1000)
        )
        evento_integracion = EventoInteraccionAtribuidaRecibida(data=payload)
        self._publicar_mensaje(
            evento_integracion, topico, EventoInteraccionAtribuidaRecibida
        )