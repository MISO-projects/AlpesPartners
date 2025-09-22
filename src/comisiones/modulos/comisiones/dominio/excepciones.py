
from comisiones.seedwork.dominio.excepciones import ExcepcionDominio

class ComisionExcepcion(ExcepcionDominio):

    pass

class ComisionYaConfirmadaExcepcion(ComisionExcepcion):

    pass

class ComisionYaRevertidaExcepcion(ComisionExcepcion):

    pass

class EstadoComisionInvalidoExcepcion(ComisionExcepcion):

    pass

class MontoComisionInvalidoExcepcion(ComisionExcepcion):

    pass

class ConfiguracionComisionInvalidaExcepcion(ComisionExcepcion):

    pass

class PoliticaFraudeInvalidaExcepcion(ComisionExcepcion):

    pass

class InteraccionNoValidaParaComisionExcepcion(ComisionExcepcion):

    pass

class ComisionNoEncontradaExcepcion(ComisionExcepcion):

    pass

class LoteComisionesInvalidoExcepcion(ComisionExcepcion):

    pass

class TipoComisionNoValidoExcepcion(Exception):
    def __init__(self, mensaje='No existe una fabrica para el tipo solicitado'):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)

