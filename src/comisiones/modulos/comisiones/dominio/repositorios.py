
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from comisiones.modulos.comisiones.dominio.entidades import Comision
from comisiones.modulos.comisiones.dominio.objetos_valor import EstadoComision
from datetime import datetime

class RepositorioComision(ABC):

    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Comision:

        ...

    @abstractmethod
    def obtener_por_interaccion(self, id_interaccion: UUID) -> Comision:

        ...

    @abstractmethod
    def obtener_por_campania(self, id_campania: UUID) -> List[Comision]:

        ...

    @abstractmethod
    def obtener_por_estado(self, estado: EstadoComision) -> List[Comision]:

        ...

    @abstractmethod
    def obtener_reservadas_vencidas(self, fecha_limite: datetime) -> List[Comision]:

        ...

    @abstractmethod
    def obtener_para_lote(self, limite: int = 100) -> List[Comision]:

        ...

    @abstractmethod
    def obtener_todos(self) -> List[Comision]:

        ...

    @abstractmethod
    def agregar(self, comision: Comision):

        ...

    @abstractmethod
    def actualizar(self, comision: Comision):

        ...

    @abstractmethod
    def eliminar(self, comision_id: UUID):

        ...

    @abstractmethod
    def obtener_por_journey_id(self, journey_id: UUID) -> Comision:

        ...

class RepositorioConfiguracionComision(ABC):

    @abstractmethod
    def obtener_por_campania(self, id_campania: UUID):

        ...

    @abstractmethod
    def obtener_por_tipo_interaccion(self, tipo_interaccion: str):

        ...

    @abstractmethod
    def obtener_default(self):

        ...

class RepositorioPoliticaFraude(ABC):

    @abstractmethod
    def obtener_por_campania(self, id_campania: UUID):

        ...

    @abstractmethod
    def obtener_default(self):

        ...
