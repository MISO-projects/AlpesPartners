
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.getenv("COMISIONES_DATABASE_URL", "sqlite:///./comisiones.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=os.getenv("DB_ECHO", "false").lower() == "true"
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("DB_ECHO", "false").lower() == "true"
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)

Base = declarative_base()

class DatabaseManager:
    
    def __init__(self):
        self.engine = engine
        self.session = session
        self.Base = Base
    
    def create_tables(self):
        Base.metadata.create_all(bind=engine)
    
    def drop_tables(self):
        Base.metadata.drop_all(bind=engine)
    
    def get_session(self):
        return session
    
    def close_session(self):
        session.remove()

db = DatabaseManager()

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
