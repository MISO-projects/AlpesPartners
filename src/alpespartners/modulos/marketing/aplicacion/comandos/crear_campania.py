from alpespartners.seedwork.aplicacion.comandos import Comando, ComandoHandler
from datetime import datetime


class CrearCampania(Comando):
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str
    tipo: str
    segmento: str


class CrearCampaniaHandler(ComandoHandler): ...
