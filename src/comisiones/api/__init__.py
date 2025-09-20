import os

from flask import Flask, jsonify
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import comisiones.modulos.comisiones.aplicacion 


def importar_modelos_alchemy():
    import comisiones.modulos.comisiones.infraestructura.dto 


def comenzar_consumidor(app):
    import threading
    import comisiones.modulos.comisiones.infraestructura.consumidores as consumidores_comisiones
    
    # Consumidor de eventos de atribución
    consumidor_atribucion = consumidores_comisiones.ConsumidorEventosAtribucion()
    threading.Thread(
        target=consumidor_atribucion.suscribirse_a_eventos_atribucion, args=[app]
    ).start()
    
    # Consumidor de eventos de reversión
    consumidor_reversion = consumidores_comisiones.ConsumidorComandosReversion()
    threading.Thread(
        target=consumidor_reversion.suscribirse_a_comandos_reversion, args=[app]
    ).start()


def create_app(configuracion={}):
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "alpespartners.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

    from comisiones.config.mongo import init_mongo
    with app.app_context():
        if not app.config.get('TESTING'):
            init_mongo()

    registrar_handlers()

    with app.app_context():
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    from . import comisiones

    app.register_blueprint(comisiones.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Comisiones API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
