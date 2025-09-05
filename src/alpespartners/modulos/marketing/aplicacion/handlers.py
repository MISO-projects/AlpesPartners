from alpespartners.seedwork.aplicacion.handlers import Handler


class HandlerInteraccionDominio(Handler):
    @staticmethod
    def handle_interaccion_registrada(evento):
        print('================ INTERACCION REGISTRADA ===========')
        print(evento)
