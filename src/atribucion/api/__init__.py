import os
from flask import Flask, jsonify


basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import atribucion.modulos.atribucion.aplicacion


def comenzar_consumidor(app):
    """Inicia el consumidor de eventos en un hilo separado"""
    import threading
    import atribucion.modulos.atribucion.infraestructura.consumidores as consumidores_atribucion
    
    consumidor = consumidores_atribucion.ConsumidorInteracciones()
    threading.Thread(
        target=consumidor.suscribirse_a_eventos_interaccion, args=[app]
    ).start()


def create_app(configuracion={}):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e33d'
    app.config['TESTING'] = configuracion.get('TESTING')
    
    # Initialize MongoDB
    from atribucion.config.mongo import init_mongo
    with app.app_context():
        if not app.config.get('TESTING'):
            init_mongo()
    
    registrar_handlers()
    
    # Iniciar consumidor de eventos
    with app.app_context():
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)
    
    @app.route("/health")
    def health():
        return {"status": "up"}
    
    return app