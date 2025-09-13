from abc import ABC
from atribucion.seedwork.dominio.repositorios import Repositorio
from .entidades import Journey

class RepositorioJourney(Repositorio, ABC):
    
    def obtener_por_usuario(self, usuario_id: str) -> Journey:
        ...