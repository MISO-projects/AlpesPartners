from marketing.seedwork.aplicacion.comandos import Comando, ComandoHandler
from marketing.modulos.campanias.dominio.repositorios import RepositorioCampania
from marketing.modulos.campanias.infraestructura.fabricas import FabricaRepositorio
from marketing.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from marketing.seedwork.aplicacion.comandos import ejecutar_commando as comando
from dataclasses import dataclass
import uuid


@dataclass
class ActivarCampania(Comando):
    id_campania: str


class ActivarCampaniaHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        
    def handle(self, comando: ActivarCampania):
        try:
            repositorio = self._fabrica_repositorio.crear_objeto(RepositorioCampania.__class__)
            campania = repositorio.obtener_por_id(uuid.UUID(comando.id_campania))

            if not campania:
                raise Exception(f"Campaña con ID {comando.id_campania} no encontrada")

            campania.activar_campania()

            # Usar direct save en lugar de unidad de trabajo para background consumers
            try:
                from flask import has_request_context
                if has_request_context():
                    # En contexto HTTP, usar unidad de trabajo
                    UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, campania)
                    UnidadTrabajoPuerto.savepoint()
                    UnidadTrabajoPuerto.commit()
                else:
                    # En background, guardar directamente
                    repositorio.actualizar(campania)
            except ImportError:
                # Fallback si Flask no está disponible
                repositorio.actualizar(campania)

            print(f" Campaña '{campania.nombre}' activada exitosamente")

            # Publicar evento de campaña activada
            self._publicar_evento_campania_activada(campania)

            return campania

        except Exception as e:
            try:
                from flask import has_request_context
                if has_request_context():
                    UnidadTrabajoPuerto.rollback()
            except ImportError:
                pass
            print(f" Error activando campaña: {e}")
            raise e

    def _publicar_evento_campania_activada(self, campania):
        """Publica evento de campaña activada al tópico correspondiente"""
        try:
            from marketing.modulos.campanias.infraestructura.despachadores import DespachadorMarketing

            # Crear el evento de dominio
            from datetime import datetime
            evento_dominio = type('EventoCampaniaActivada', (), {
                'id_campania': campania.id,
                'nombre': campania.nombre,
                'tipo': campania.tipo,
                'fecha_inicio': campania.fecha_inicio,
                'fecha_fin': campania.fecha_fin,
                'fecha_activacion': datetime.now(),
                'segmento': campania.segmento
            })()

            despachador = DespachadorMarketing()
            despachador.publicar_campania_activada(evento_dominio)
            print(f" Evento 'CampaniaActivada' publicado para campaña: {campania.nombre}")

        except Exception as e:
            print(f" Error publicando evento de campaña activada: {e}")
            # No lanzamos excepción para no fallar la activación de la campaña

@comando.register(ActivarCampania)
def ejecutar_comando(comando: ActivarCampania):
    handler = ActivarCampaniaHandler()
    handler.handle(comando)