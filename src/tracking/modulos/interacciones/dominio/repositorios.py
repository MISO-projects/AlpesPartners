"""Interfaces para los repositorios del dominio de tracking

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de tracking

"""

from abc import ABC, abstractmethod
import uuid
from tracking.modulos.interacciones.dominio.entidades import Interaccion
from tracking.seedwork.dominio.repositorios import Repositorio


class RepositorioInteraccion(Repositorio, ABC):

    @abstractmethod
    def obtener_por_ids(self, ids: list[uuid.UUID]) -> list[Interaccion]: ...
