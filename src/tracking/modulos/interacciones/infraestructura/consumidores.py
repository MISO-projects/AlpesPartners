import pulsar, _pulsar
from pulsar.schema import *
from tracking.modulos.interacciones.infraestructura.schema.v1.eventos import (
    EventoCampaniaActivada,
)
from tracking.modulos.interacciones.infraestructura.schema.v1.comandos import (
    ComandoDescartarInteracciones,
    ComandoRegistrarInteraccion,
)
from tracking.seedwork.infraestructura import utils
import traceback
from tracking.seedwork.aplicacion.comandos import ejecutar_commando
from tracking.modulos.interacciones.aplicacion.comandos.descartar_interacciones import (
    DescartarInteracciones,
)
from tracking.modulos.interacciones.aplicacion.comandos.registrar_interaccion import (
    RegistrarInteraccion,
)


class ConsumidorEventosInteracciones:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_eventos(self, app=None):
        if not app:
            return

        self.app = app

        try:
            self.cliente = pulsar.Client(
                f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            self.consumidor = self.cliente.subscribe(
                'campania-activada',
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='alpespartners-sub-eventos',
                schema=AvroSchema(EventoCampaniaActivada),
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            print(
                                f'Evento recibido en tracking: {mensaje.value().data}'
                            )
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f"Error procesando InteraccionRegistrada: {e}")
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)
        except Exception as e:
            print(f"Error configurando consumidor de atribución: {e}")
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()


class ConsumidorComandosInteracciones:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_comandos(self, app=None):
        if not app:
            return

        self.app = app

        try:
            self.cliente = pulsar.Client(
                f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            self.consumidor = self.cliente.subscribe(
                'descartar-interacciones-comando',
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='tracking-sub-comandos',
                schema=AvroSchema(ComandoDescartarInteracciones),
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_mensaje_con_comando(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f"Error procesando ComandoDescartarInteraccion: {e}")
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)
        except Exception as e:
            print(f"Error configurando consumidor de COMANDOS: {e}")
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_mensaje_con_comando(self, mensaje):

        payload = mensaje.value().data
        print(f'Comando recibido en tracking: {payload}')
        comando = DescartarInteracciones(
            id_correlacion=payload.id_correlacion, interacciones=payload.interacciones
        )
        ejecutar_commando(comando)


class ConsumidorComandosRegistrarInteraccion:
    def __init__(self):
        self.cliente = None
        self.consumidor = None

    def suscribirse_a_comandos_registrar(self, app=None):
        if not app:
            return

        self.app = app

        try:
            self.cliente = pulsar.Client(
                f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(pulsar.LoggerLevel.Error),
            )
            self.consumidor = self.cliente.subscribe(
                'comando-registrar-interaccion',
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='tracking-sub-registrar-comandos',
            )

            while True:
                mensaje = self.consumidor.receive()
                try:
                    with self.app.app_context():
                        with self.app.test_request_context():
                            self._procesar_comando_registrar_interaccion(mensaje)
                    self.consumidor.acknowledge(mensaje)
                except Exception as e:
                    print(f"Error procesando ComandoRegistrarInteraccion: {e}")
                    traceback.print_exc()
                    self.consumidor.acknowledge(mensaje)
        except Exception as e:
            print(f"Error configurando consumidor de COMANDOS REGISTRAR: {e}")
            traceback.print_exc()
        finally:
            if self.cliente:
                self.cliente.close()

    def _procesar_comando_registrar_interaccion(self, mensaje):
        import json
        from datetime import datetime
        from tracking.modulos.interacciones.aplicacion.dto import (
            IdentidadUsuarioDTO,
            ParametrosTrackingDTO,
            ElementoObjetivoDTO,
            ContextoInteraccionDTO
        )

        # Deserializar JSON
        mensaje_json = json.loads(mensaje.value().decode('utf-8'))
        payload = mensaje_json['data']
        print(f'Comando RegistrarInteraccion recibido en tracking: {payload}')

        # Convertir marca_temporal de string a datetime si es necesario
        marca_temporal = payload['marca_temporal']
        if isinstance(marca_temporal, str):
            marca_temporal = datetime.fromisoformat(marca_temporal.replace('Z', '+00:00'))

        # Crear DTOs mapeando campos correctamente
        identidad_usuario = IdentidadUsuarioDTO(
            id_usuario=payload['identidad_usuario'],
            id_anonimo="",
            direccion_ip="",
            agente_usuario=""
        )

        # Mapear parametros_tracking a los campos del DTO
        params = payload['parametros_tracking']
        parametros_tracking = ParametrosTrackingDTO(
            fuente=params.get('utm_source', ''),
            medio=params.get('utm_medium', ''),
            campania=params.get('utm_campaign', ''),
            contenido=params.get('utm_content', ''),
            termino=params.get('utm_term', ''),
            id_afiliado=params.get('affiliate_id', '')
        )

        elemento_objetivo = ElementoObjetivoDTO(
            id_elemento=payload['elemento_objetivo'],
            tipo_elemento="",
            nombre_elemento="",
            url_elemento="",
            texto_elemento="",
            imagen_elemento="",
            video_elemento="",
            audio_elemento="",
            link_elemento="",
            texto_alternativo_elemento="",
            titulo_elemento=""
        )

        # Mapear contexto a los campos del DTO
        ctx = payload['contexto']
        contexto = ContextoInteraccionDTO(
            url_pagina=ctx.get('pagina', ''),
            url_referente="",
            informacion_dispositivo=f"device:{ctx.get('device', '')},browser:{ctx.get('browser', '')},seccion:{ctx.get('seccion', '')}"
        )

        comando = RegistrarInteraccion(
            id_correlacion=mensaje_json['id'],  # Usar el ID del mensaje como correlación
            tipo=payload['tipo'],
            marca_temporal=marca_temporal,
            identidad_usuario=identidad_usuario,
            parametros_tracking=parametros_tracking,
            elemento_objetivo=elemento_objetivo,
            contexto=contexto
        )
        ejecutar_commando(comando)
