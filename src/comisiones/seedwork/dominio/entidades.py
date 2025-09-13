
from dataclasses import dataclass, field
from .eventos import EventoDominio
from .mixins import ValidarReglasMixin
from .reglas import IdEntidadEsInmutable
from .excepciones import IdDebeSerInmutableExcepcion
from datetime import datetime
import uuid

@dataclass
class Entidad:
    id: uuid.UUID = field(default_factory=uuid.uuid4, hash=True)
    fecha_creacion: datetime =  field(default=datetime.now())
    fecha_actualizacion: datetime = field(default=datetime.now())

    @classmethod
    def siguiente_id(self) -> uuid.UUID:
        return uuid.uuid4()

@dataclass
class AgregacionRaiz(Entidad, ValidarReglasMixin):
    eventos: list[EventoDominio] = field(default_factory=list)

    def agregar_evento(self, evento: EventoDominio):
        self.eventos.append(evento)
    
    def limpiar_eventos(self):
        self.eventos = list()

@dataclass
class Locacion(Entidad):
    def __str__(self) -> str:
        ...