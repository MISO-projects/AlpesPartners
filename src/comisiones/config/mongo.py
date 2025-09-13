
import os
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)

class MongoConfig:
    
    def __init__(self):
        self.connection_string = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        self.database_name = os.getenv("MONGODB_DATABASE", "comisiones")
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
        if not self.database:
            self.connect()
        return self.database
        
    def get_collection(self, collection_name: str):
        database = self.get_database()
        return database[collection_name]

mongo_config = MongoConfig()

def init_mongo():
    """Initialize MongoDB connection"""
    try:
        mongo_config.connect()
        print("✅ MongoDB connection established for comisiones")
        
    except Exception as e:
        print(f"❌ MongoDB initialization failed for comisiones: {e}")
        raise
