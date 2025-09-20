from marketing.seedwork.aplicacion.comandos import Comando, ComandoHandler
from marketing.modulos.campanias.dominio.entidades import Campania, EstadoCampania
from marketing.modulos.campanias.dominio.objetos_valor import (
    SegmentoAudiencia,
    ConfiguracionCampania,
    MetricasCampania,
)
from marketing.modulos.campanias.dominio.repositorios import RepositorioCampania
from marketing.modulos.campanias.infraestructura.fabricas import FabricaRepositorio
from marketing.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from datetime import datetime
from marketing.seedwork.aplicacion.comandos import ejecutar_commando as comando
from dataclasses import dataclass


@dataclass
class CrearCampania(Comando):
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    tipo: str = "DIGITAL"
    edad_minima: int = None
    edad_maxima: int = None
    genero: str = None
    ubicacion: str = None
    intereses: list = None
    presupuesto: float = 0.0
    canales: list = None


class CrearCampaniaHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

        
    def handle(self, comando: CrearCampania):
        try:
            segmento = SegmentoAudiencia(
                edad_minima=comando.edad_minima,
                edad_maxima=comando.edad_maxima,
                genero=comando.genero,
                ubicacion=comando.ubicacion,
                intereses=comando.intereses or [],
            )

            configuracion = ConfiguracionCampania(
                presupuesto=comando.presupuesto,
                canales=comando.canales or ["WEB", "EMAIL"],
            )

            campania = Campania(
                nombre=comando.nombre,
                descripcion=comando.descripcion,
                fecha_inicio=comando.fecha_inicio,
                fecha_fin=comando.fecha_fin,
                tipo=comando.tipo,
                segmento=segmento,
                configuracion=configuracion,
                metricas=MetricasCampania(),
            )

            campania.crear_campania()

            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioCampania.__class__
            )

            # Usar direct save en lugar de unidad de trabajo para background consumers
            try:
                from flask import has_request_context
                if has_request_context():
                    # En contexto HTTP, usar unidad de trabajo
                    UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, campania)
                    UnidadTrabajoPuerto.savepoint()
                    UnidadTrabajoPuerto.commit()
                else:
                    # En background, guardar directamente
                    repositorio.agregar(campania)
            except ImportError:
                # Fallback si Flask no está disponible
                repositorio.agregar(campania)

            print(f" Campaña '{campania.nombre}' creada exitosamente")

            # Publicar evento de campaña creada
            self._publicar_evento_campania_creada(campania)

            return campania

        except Exception as e:
            try:
                from flask import has_request_context
                if has_request_context():
                    UnidadTrabajoPuerto.rollback()
            except ImportError:
                pass
            print(f" Error creando campaña: {e}")
            raise e

    def _publicar_evento_campania_creada(self, campania):
        """Publica evento de campaña creada al tópico correspondiente"""
        try:
            from marketing.modulos.campanias.infraestructura.despachadores import DespachadorMarketing

            # Crear el evento de dominio
            evento_dominio = type('EventoCampaniaCreada', (), {
                'id_campania': campania.id,
                'nombre': campania.nombre,
                'tipo': campania.tipo,
                'fecha_inicio': campania.fecha_inicio,
                'fecha_fin': campania.fecha_fin,
                'segmento': campania.segmento
            })()

            despachador = DespachadorMarketing()
            despachador.publicar_campania_creada(evento_dominio)
            print(f" Evento 'CampaniaCreada' publicado para campaña: {campania.nombre}")

        except Exception as e:
            print(f" Error publicando evento de campaña creada: {e}")
            # No lanzamos excepción para no fallar la creación de la campaña


@comando.register(CrearCampania)
def ejecutar_comando(comando: CrearCampania):
    handler = CrearCampaniaHandler()
    handler.handle(comando)
