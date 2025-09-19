import os

from flask import Flask, jsonify
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import marketing.modulos.campanias.aplicacion


def importar_modelos_alchemy():
    import marketing.modulos.sagas.infraestructura.dto


def comenzar_consumidor(app):
    import threading
    from marketing.modulos.sagas.infraestructura.consumidores import (
        ConsumidorInteracciones,
        ConsumidorAtribucion,
        ConsumidorAtribucionRevertida,
        ConsumidorComisiones,
        ConsumidorComisionesRevertidas,
        ConsumidorFraude,
        ConsumidorInteraccionDescartada,
    )

    consumidor_interacciones = ConsumidorInteracciones()
    consumidor_interaccion_descartada = ConsumidorInteraccionDescartada()
    consumidor_atribucion = ConsumidorAtribucion()
    consumidor_atribucion_revertida = ConsumidorAtribucionRevertida()
    consumidor_comisiones = ConsumidorComisiones()
    consumidor_comisiones_revertidas = ConsumidorComisionesRevertidas()
    consumidor_fraude = ConsumidorFraude()
    threading.Thread(
        target=consumidor_interacciones.suscribirse_a_eventos, args=[app]
    ).start()
    threading.Thread(
        target=consumidor_interaccion_descartada.suscribirse_a_eventos, args=[app]
    ).start()
    threading.Thread(
        target=consumidor_atribucion.suscribirse_a_eventos, args=[app]
    ).start()
    threading.Thread(
        target=consumidor_atribucion_revertida.suscribirse_a_eventos, args=[app]
    ).start()
    threading.Thread(
        target=consumidor_comisiones.suscribirse_a_eventos, args=[app]
    ).start()
    threading.Thread(
        target=consumidor_comisiones_revertidas.suscribirse_a_eventos, args=[app]
    ).start()
    threading.Thread(target=consumidor_fraude.suscribirse_a_eventos, args=[app]).start()


def create_app(configuracion={}):
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

    # Initialize databases
    from marketing.config.mongo import init_mongo
    from marketing.config.db import init_postgres, db
    init_postgres(app)
    importar_modelos_alchemy()

    with app.app_context():
        if not app.config.get('TESTING'):
            init_mongo()
            db.create_all()

    registrar_handlers()

    with app.app_context():
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    from . import marketing

    app.register_blueprint(marketing.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
