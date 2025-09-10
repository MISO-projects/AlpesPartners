"""Excepciones del dominio de marketing

En este archivo usted encontrará las diferentes excepciones específicas
del dominio de marketing

"""

from marketing.seedwork.dominio.excepciones import ExcepcionDominio


class TipoCampaniaNoValidaExcepcion(ExcepcionDominio):
    def __init__(self, mensaje):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)


class CampaniaNoExisteExcepcion(ExcepcionDominio):
    def __init__(self, mensaje):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)


class EstadoCampaniaNoValidoExcepcion(ExcepcionDominio):
    def __init__(self, mensaje):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)


class NombreCampaniaNoValidoExcepcion(ExcepcionDominio):
    def __init__(self, mensaje):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)
