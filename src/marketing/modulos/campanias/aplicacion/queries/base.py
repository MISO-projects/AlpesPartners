from marketing.modulos.campanias.infraestructura.fabricas import FabricaRepositorio
from marketing.modulos.campanias.dominio.fabricas import FabricaCampania


class CampaniaQueryBaseHandler:
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_campania: FabricaCampania = FabricaCampania()

    @property
    def fabrica_campania(self) -> FabricaCampania:
        return self._fabrica_campania

    @property
    def fabrica_repositorio(self) -> FabricaRepositorio:
        return self._fabrica_repositorio
