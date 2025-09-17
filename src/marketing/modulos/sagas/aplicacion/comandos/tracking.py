from marketing.seedwork.aplicacion.comandos import Comando
import uuid


class DescartarInteraccion(Comando):
    id_interaccion: uuid.UUID
