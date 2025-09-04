"""Interfaces para los repositorios del dominio de tracking

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de tracking

"""

from abc import ABC
from alpespartners.seedwork.dominio.repositorios import Repositorio


class RepositorioInteraccion(Repositorio, ABC): ...
