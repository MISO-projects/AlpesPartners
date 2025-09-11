from flask import Flask

def create_app(configuracion={}):
    app = Flask(__name__, instance_relative_config=True)
    # TODO: Implementar la app