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
            UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, campania)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

            print(f" Campaña '{campania.nombre}' creada exitosamente")
            return campania

        except Exception as e:
            UnidadTrabajoPuerto.rollback()
            print(f" Error creando campaña: {e}")
            raise e


@comando.register(CrearCampania)
def ejecutar_comando(comando: CrearCampania):
    handler = CrearCampaniaHandler()
    handler.handle(comando)
