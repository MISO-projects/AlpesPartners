
import os
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)

class MongoConfig:
    
    def __init__(self):

        user = os.getenv('MONGODB_USER', 'admin')
        password = os.getenv('MONGODB_PASSWORD', 'admin123')
        host = os.getenv('MONGODB_HOST', 'mongodb')
        port = os.getenv('MONGODB_PORT', '27017')
        database = os.getenv('MONGODB_DATABASE', 'alpespartners')
        self.connection_string = f"mongodb://{user}:{password}@{host}:{port}/{database}?authSource=admin"
        self.database_name = database
        self.client = None
        self.database = None
        
    def connect(self):
        try:
            self.client = MongoClient(self.connection_string)
            self.database = self.client[self.database_name]
            logger.info(f"Conectado a MongoDB: {self.connection_string}")
            return True
        except Exception as e:
            logger.error(f"Error conectando a MongoDB: {e}")
            return False
            
    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Desconectado de MongoDB")
            
    def get_database(self):
        if self.database is None:
            self.connect()
        return self.database
        
    def get_collection(self, collection_name: str):
        database = self.get_database()
        return database[collection_name]

mongo_config = MongoConfig()

def init_mongo():
    try:
        mongo_config.connect()
        print("MongoDB connection established for comisiones")
        
    except Exception as e:
        print(f"MongoDB initialization failed for comisiones: {e}")
        raise
