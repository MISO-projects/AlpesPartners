import pulsar
from pulsar.schema import *
from alpespartners.modulos.tracking.infraestructura.schema.v1.eventos import (
    EventoInteraccionRegistrada,
)
from alpespartners.modulos.tracking.infraestructura.schema.v1.comandos import (
    ComandoRegistrarInteraccion,
    ComandoRegistrarInteraccionPayload,
)
from alpespartners.modulos.tracking.infraestructura.schema.v1.eventos import (
    InteraccionRegistradaPayload,
)
from alpespartners.seedwork.infraestructura import utils


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        try:
            publicador = cliente.create_producer(
                topico, schema=AvroSchema(schema)
            )
            publicador.send(mensaje)
            print(f' Mensaje Tracking publicado en tópico: {topico}')
        except Exception as e:
            print(f' Error publicando mensaje Tracking: {e}')
            print(f' [FALLBACK] Publicando mensaje {mensaje.data} en tópico {topico}')
        finally:
            if cliente:
                cliente.close()

    def publicar_evento(self, evento, topico):
        payload = InteraccionRegistradaPayload(
            tipo=evento.tipo,
            marca_temporal=int(evento.marca_temporal.timestamp() * 1000),
            identidad_usuario=evento.identidad_usuario,
            parametros_tracking=evento.parametros_tracking,
            elemento_objetivo=evento.elemento_objetivo,
            contexto=evento.contexto,
        )
        evento_integracion = EventoInteraccionRegistrada(data=payload)
        self._publicar_mensaje(
            evento_integracion, topico, AvroSchema(EventoInteraccionRegistrada)
        )

    def publicar_comando(self, comando, topico):
        payload = ComandoRegistrarInteraccionPayload(
            tipo=comando.tipo,
            marca_temporal=comando.marca_temporal,
            identidad_usuario=comando.identidad_usuario,
            parametros_tracking=comando.parametros_tracking,
            elemento_objetivo=comando.elemento_objetivo,
            contexto=comando.contexto,
        )
        comando_integracion = ComandoRegistrarInteraccion(data=payload)
        self._publicar_mensaje(
            comando_integracion, topico, AvroSchema(ComandoRegistrarInteraccion)
        )
