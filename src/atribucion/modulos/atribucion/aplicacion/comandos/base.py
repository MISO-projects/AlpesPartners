from atribucion.seedwork.aplicacion.comandos import ComandoHandler
from atribucion.modulos.atribucion.infraestructura.fabricas import FabricaRepositorio
from atribucion.modulos.atribucion.dominio.fabricas import FabricaAtribucion

class RegistrarAtribucionBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_atribucion: FabricaAtribucion = FabricaAtribucion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_atribucion(self): 
        return self._fabrica_atribucion

class RevertirAtribucionBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_atribucion: FabricaAtribucion = FabricaAtribucion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_atribucion(self): 
        return self._fabrica_atribucion
# ------------------------------------