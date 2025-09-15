from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import CollectionInvalid
import os


class MongoConfig:
    def __init__(self):
        self._client = None
        self._database = None

    def get_client(self) -> MongoClient:
        if self._client is None:
            user = os.getenv('MONGODB_USER', 'admin')
            password = os.getenv('MONGODB_PASSWORD', 'admin123')
            host = os.getenv('MONGODB_HOST', 'mongodb')
            port = os.getenv('MONGODB_PORT', '27017')
            database = os.getenv('MONGODB_DATABASE', 'alpespartners')
            
            mongo_uri = f"mongodb://{user}:{password}@{host}:{port}/{database}?authSource=admin"
            self._client = MongoClient(mongo_uri)
        return self._client

    def get_database(self, db_name: str = None) -> Database:
        if self._database is None:
            db_name = db_name or os.getenv('MONGODB_DATABASE', 'alpespartners')
            self._database = self.get_client()[db_name]
        return self._database

    def close_connection(self):
        if self._client:
            self._client.close()
            self._client = None
            self._database = None


# Global instance
mongo_config = MongoConfig()


def init_mongo():
    """Initialize MongoDB connection"""
    try:
        # Test connection
        mongo_config.get_client().admin.command('ping')
        print("✅ MongoDB connection established")
        
        
    except Exception as e:
        print(f"❌ MongoDB initialization failed: {e}")
        raise
