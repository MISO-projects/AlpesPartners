from marketing.seedwork.dominio.excepciones import ExcepcionDominio


class TipoSagaLogNoValidaExcepcion(ExcepcionDominio):
    def __init__(self, mensaje):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)
