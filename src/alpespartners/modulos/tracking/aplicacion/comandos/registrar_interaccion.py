from alpespartners.seedwork.aplicacion.comandos import Comando, ComandoHandler


class RegistrarInteraccion(Comando):
    url: str
    metodo: str
    ip: str
    user_agent: str
    tiempo_respuesta: int
    estado: int
    codigo_error: str
    mensaje_error: str
    tiempo_procesamiento: int
    tiempo_total: int
    tiempo_total_ms: int
    tiempo_total_ms: int


class RegistrarInteraccionHandler(ComandoHandler): ...
