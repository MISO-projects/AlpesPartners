import pulsar
from pulsar.schema import AvroSchema
from marketing.seedwork.infraestructura import utils
from marketing.modulos.sagas.infraestructura.schema.v1.comandos.comision import (
    ComandoRevertirComision,
    RevertirComisionPayload,
)


class DespachadorSagas:
    def __init__(self):
        self.cliente = None

    def _obtener_cliente(self):
        if not self.cliente:
            self.cliente = pulsar.Client(
                f'pulsar://{utils.broker_host()}:6650',
                logger=pulsar.ConsoleLogger(
                    pulsar.LoggerLevel.Error
                ),  # Only show errors
            )
        return self.cliente

    def _publicar_mensaje(self, mensaje, topico, schema_class):
        cliente = self._obtener_cliente()
        try:
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema_class))
            publicador.send(mensaje)
            print(f'{schema_class.__name__} publicado en tópico: {topico}')
        except Exception as e:
            print(f' Error publicando evento Marketing: {e}')
            raise e
        finally:
            if cliente:
                cliente.close()

    def publicar_comando_revertir_comision(self, comando):
        payload = RevertirComisionPayload(
            id_correlacion=comando.id_correlacion,
            journey_id=comando.journey_id,
            motivo=comando.motivo
        )
        comando_integracion = ComandoRevertirComision(data=payload)
        self._publicar_mensaje(
            comando_integracion,
            "revertir-comision-comando",
            ComandoRevertirComision
        )