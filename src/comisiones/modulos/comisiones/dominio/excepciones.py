
from seedwork.dominio.excepciones import ExcepcionDominio

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
