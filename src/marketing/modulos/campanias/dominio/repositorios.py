"""Interfaces para los repositorios del dominio de marketing

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de marketing

"""

from abc import ABC, abstractmethod
from uuid import UUID
from marketing.seedwork.dominio.repositorios import Repositorio
from marketing.modulos.campanias.dominio.entidades import Campania


class RepositorioCampania(Repositorio, ABC):
    
    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Campania:
        """Obtiene una campaña por su nombre"""
        ...

    @abstractmethod
    def obtener_activas(self) -> list[Campania]:
        """Obtiene todas las campañas activas"""
        ...
        
    @abstractmethod
    def obtener_por_segmento(self, ubicacion: str = None, edad_minima: int = None, edad_maxima: int = None) -> list[Campania]:
        """Obtiene campañas filtradas por segmento de audiencia"""
        ...
