import pulsar
from pulsar.schema import *
import uuid
from datetime import datetime

from . import utils


class DespachadorMarketing:
    def __init__(self):
        ...

    async def publicar_comando_crear_campania(self, datos_campania):
        """
        Publica un comando para crear una campaña de forma asíncrona
        """
        # Convertir fechas a timestamps
        if hasattr(datos_campania["fecha_inicio"], 'timestamp'):
            fecha_inicio_ts = int(datos_campania["fecha_inicio"].timestamp() * 1000)
        else:
            fecha_inicio_ts = utils.time_millis()

        if hasattr(datos_campania["fecha_fin"], 'timestamp'):
            fecha_fin_ts = int(datos_campania["fecha_fin"].timestamp() * 1000)
        else:
            fecha_fin_ts = utils.time_millis()

        payload = dict(
            nombre=datos_campania["nombre"],
            descripcion=datos_campania["descripcion"],
            fecha_inicio=fecha_inicio_ts,
            fecha_fin=fecha_fin_ts,
            tipo=datos_campania["tipo"],
            segmento={
                'edad_minima': str(datos_campania.get("edad_minima", "")),
                'edad_maxima': str(datos_campania.get("edad_maxima", "")),
                'genero': datos_campania.get("genero", ""),
                'ubicacion': datos_campania.get("ubicacion", ""),
                'intereses': ','.join(datos_campania.get("intereses", []))
            },
            configuracion={
                'presupuesto': str(datos_campania.get("presupuesto", "")),
                'canales': ','.join(datos_campania.get("canales", []))
            }
        )

        # Crear el comando usando el schema AVRO
        comando_data = {
            'id': str(uuid.uuid4()),
            'time': utils.time_millis(),
            'specversion': "v1",
            'type': "ComandoCrearCampania",
            'ingestion': utils.time_millis(),
            'datacontenttype': "AVRO",
            'service_name': "BFF Web",
            'data': payload
        }

        await self.publicar_mensaje(comando_data, "comando-crear-campania", "public/default/comando-crear-campania")

    async def publicar_comando_activar_campania(self, id_campania):
        """
        Publica un comando para activar una campaña de forma asíncrona
        """
        payload = dict(
            id_campania=id_campania,
            fecha_activacion=utils.time_millis()
        )

        comando = dict(
            id=str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion="v1",
            type="ComandoActivarCampania",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name="BFF Web",
            data=payload
        )

        await self.publicar_mensaje(comando, "comando-activar-campania", "public/default/comando-activar-campania")

    async def publicar_mensaje(self, mensaje, topico, schema_path):
        cliente = None
        try:
            import json
            cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')

            # Crear productor sin schema
            publicador = cliente.create_producer(topico)

            # Serializar mensaje a JSON bytes
            mensaje_json = json.dumps(mensaje).encode('utf-8')
            publicador.send(mensaje_json)
            print(f"✓ Comando publicado: {mensaje.get('type', 'desconocido')}")

        except Exception as e:
            print(f"✗ Error publicando comando: {e}")
            raise e
        finally:
            if cliente:
                cliente.close()