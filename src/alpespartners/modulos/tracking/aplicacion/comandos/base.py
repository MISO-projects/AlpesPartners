from alpespartners.modulos.tracking.dominio.fabricas import FabricaInteraccion
from alpespartners.modulos.tracking.infraestructura.fabricas import FabricaRepositorio


class CrearInteraccionBaseHandler:
    def __init__(self):
        self._fabrica_interaccion: FabricaInteraccion = FabricaInteraccion()
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()

    @property
    def fabrica_interaccion(self) -> FabricaInteraccion:
        return self._fabrica_interaccion

    @property
    def fabrica_repositorio(self) -> FabricaRepositorio:
        return self._fabrica_repositorio
