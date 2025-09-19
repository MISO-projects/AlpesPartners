import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()

Base = db.declarative_base()

def get_database_uri():
    """Get the appropriate database URI based on environment variables."""
    # PostgreSQL configuration from environment variables
    user = os.getenv('POSTGRES_USER', 'root')
    password = os.getenv('POSTGRES_PASSWORD', 'saga_log_pass')
    host = os.getenv('POSTGRES_HOST', 'saga_log_db')
    port = os.getenv('POSTGRES_PORT', '5432')
    database = os.getenv('POSTGRES_DB', 'saga_log_db')
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def init_postgres(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # PostgreSQL-specific configurations
    if 'postgresql' in app.config["SQLALCHEMY_DATABASE_URI"]:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'connect_args': {
                'connect_timeout': 60,
                'application_name': 'marketing_service'
            }
        }
    
    db.init_app(app)
    