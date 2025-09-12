class TipoInteraccionNoValidoExcepcion(Exception):
    def __init__(self, mensaje='No existe una fabrica para el tipo solicitado'):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)
