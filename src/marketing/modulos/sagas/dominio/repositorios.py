"""Interfaces para los repositorios del dominio de marketing

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de marketing

"""

from abc import ABC, abstractmethod
from uuid import UUID
from marketing.seedwork.dominio.entidades import Entidad


class RepositorioSagaLog(ABC):
    @abstractmethod
    def obtener_todos(self, id_correlacion: UUID) -> list[Entidad]:
        ...

    @abstractmethod
    def agregar(self, entity: Entidad):
        ...





    