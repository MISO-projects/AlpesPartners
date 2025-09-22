import pulsar, _pulsar
from pulsar.schema import *
from marketing.modulos.campanias.infraestructura.schema.v1.comandos.campania import (
    ComandoCrearCampania,
    ComandoActivarCampania
)
from marketing.seedwork.infraestructura import utils
from marketing.config.db import db
from marketing.modulos.campanias.aplicacion.comandos.crear_campania import CrearCampania
from marketing.modulos.campanias.aplicacion.comandos.activar_campania import ActivarCampania
from marketing.seedwork.aplicacion.comandos import ejecutar_commando
import traceback


def _procesar_comando_crear_campania(mensaje_crear, consumidor_crear):
    """Procesa comando de crear campaña dentro del contexto de Flask"""
    import json
    from datetime import datetime

    # Deserializar bytes a JSON
    datos_comando = json.loads(mensaje_crear.value().decode('utf-8'))
    datos_crear = datos_comando.get('data', {})  # Payload del comando
    print(f'Comando crear campaña recibido: {datos_crear}')

    # Convertir timestamps a datetime
    fecha_inicio = datetime.fromtimestamp(datos_crear['fecha_inicio'] / 1000)
    fecha_fin = datetime.fromtimestamp(datos_crear['fecha_fin'] / 1000)

    # Procesar segmento
    segmento_dict = datos_crear['segmento']
    edad_minima = int(segmento_dict.get('edad_minima', 0)) if segmento_dict.get('edad_minima') else None
    edad_maxima = int(segmento_dict.get('edad_maxima', 0)) if segmento_dict.get('edad_maxima') else None
    intereses = segmento_dict.get('intereses', '').split(',') if segmento_dict.get('intereses') else []

    # Procesar configuración
    config_dict = datos_crear['configuracion']
    presupuesto = float(config_dict.get('presupuesto', 0)) if config_dict.get('presupuesto') else 0.0
    canales = config_dict.get('canales', '').split(',') if config_dict.get('canales') else []

    comando = CrearCampania(
        nombre=datos_crear['nombre'],
        descripcion=datos_crear['descripcion'],
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        tipo=datos_crear['tipo'],
        edad_minima=edad_minima,
        edad_maxima=edad_maxima,
        genero=segmento_dict.get('genero', ''),
        ubicacion=segmento_dict.get('ubicacion', ''),
        intereses=intereses,
        presupuesto=presupuesto,
        canales=canales
    )

    ejecutar_commando(comando)
    consumidor_crear.acknowledge(mensaje_crear)


def _procesar_comando_activar_campania(mensaje_activar, consumidor_activar):
    """Procesa comando de activar campaña dentro del contexto de Flask"""
    import json

    # Deserializar bytes a JSON
    datos_comando = json.loads(mensaje_activar.value().decode('utf-8'))
    datos_activar = datos_comando.get('data', {})  # Payload del comando
    print(f'Comando activar campaña recibido: {datos_activar}')

    comando = ActivarCampania(
        id_campania=datos_activar['id_campania']
    )

    ejecutar_commando(comando)
    consumidor_activar.acknowledge(mensaje_activar)


def suscribirse_a_eventos(app=None):
    import time
    cliente = None
    consumidor_crear = None
    consumidor_activar = None

    def conectar_con_retry():
        nonlocal cliente, consumidor_crear, consumidor_activar
        max_reintentos = 5
        for intento in range(max_reintentos):
            try:
                print(f"🔄 Intento {intento + 1}/{max_reintentos} conectando a Pulsar...")
                cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')

                # Consumidor para comandos de crear campaña (sin schema)
                consumidor_crear = cliente.subscribe(
                    'comando-crear-campania',
                    consumer_type=_pulsar.ConsumerType.Shared,
                    subscription_name='marketing-sub-crear-campania'
                )

                # Consumidor para comandos de activar campaña (sin schema)
                consumidor_activar = cliente.subscribe(
                    'comando-activar-campania',
                    consumer_type=_pulsar.ConsumerType.Shared,
                    subscription_name='marketing-sub-activar-campania'
                )
                print("✅ Conectado exitosamente a Pulsar")
                return True
            except Exception as e:
                print(f"❌ Intento {intento + 1} falló: {e}")
                if cliente:
                    try:
                        cliente.close()
                    except:
                        pass
                    cliente = None
                if intento < max_reintentos - 1:
                    tiempo_espera = 2 ** intento  # Backoff exponencial
                    print(f"⏳ Esperando {tiempo_espera}s antes del siguiente intento...")
                    time.sleep(tiempo_espera)
        return False

    try:
        if not conectar_con_retry():
            print("❌ No se pudo conectar a Pulsar después de varios intentos")
            return

        while True:
            try:
                # Verificar mensajes de crear campaña
                try:
                    mensaje_crear = consumidor_crear.receive(timeout_millis=100)
                    if mensaje_crear:
                        # Procesar dentro del contexto de la app
                        if app:
                            with app.app_context():
                                _procesar_comando_crear_campania(mensaje_crear, consumidor_crear)
                        else:
                            _procesar_comando_crear_campania(mensaje_crear, consumidor_crear)
                except Exception as e:
                    if "Timeout" not in str(e) and "TimeOut" not in str(e):
                        print(f'Error procesando comando crear campaña: {e}')

                # Verificar mensajes de activar campaña
                try:
                    mensaje_activar = consumidor_activar.receive(timeout_millis=100)
                    if mensaje_activar:
                        # Procesar dentro del contexto de la app
                        if app:
                            with app.app_context():
                                _procesar_comando_activar_campania(mensaje_activar, consumidor_activar)
                        else:
                            _procesar_comando_activar_campania(mensaje_activar, consumidor_activar)
                except Exception as e:
                    if "Timeout" not in str(e) and "TimeOut" not in str(e):
                        print(f'Error procesando comando activar campaña: {e}')

            except Exception as e:
                if "Disconnected" in str(e) or "Connection" in str(e):
                    print(f'🔄 Conexión perdida, reintentando...')
                    if conectar_con_retry():
                        continue
                    else:
                        break
                else:
                    print(f'Error general en consumer: {e}')

        cliente.close()
    except Exception as e:
        print(f'ERROR: Suscribiéndose a comandos de marketing: {e}')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos(): ...
