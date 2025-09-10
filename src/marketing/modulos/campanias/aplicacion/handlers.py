from marketing.seedwork.aplicacion.handlers import Handler
from marketing.modulos.campanias.infraestructura.despachadores import DespachadorMarketing
from marketing.modulos.campanias.dominio.repositorios import RepositorioCampania
from marketing.modulos.campanias.infraestructura.fabricas import FabricaRepositorio
from marketing.seedwork.infraestructura.uow import UnidadTrabajoPuerto


class HandlerCampaniaIntegracion(Handler):

    @staticmethod
    def handle_campania_creada(evento):
        despachador = DespachadorMarketing()
        despachador.publicar_campania_creada(evento)
        print(f" Evento CampaniaCreada publicado vía Pulsar: {evento.nombre}")

    @staticmethod  
    def handle_campania_activada(evento):
        despachador = DespachadorMarketing()
        despachador.publicar_campania_activada(evento)
        print(f" Evento CampaniaActivada publicado vía Pulsar: {evento.nombre}")

    @staticmethod
    def handle_campania_desactivada(evento):
        despachador = DespachadorMarketing()
        despachador.publicar_campania_desactivada(evento)
        print(f" Evento CampaniaDesactivada publicado vía Pulsar: {evento.razon}")

    @staticmethod
    def handle_interaccion_recibida(evento):
        despachador = DespachadorMarketing()
        despachador.publicar_interaccion_recibida(evento)
        print(f" Evento InteraccionRecibida publicado vía Pulsar para campaña: {evento.id_campania}")

