from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from settings import Config
load_dotenv()

Base = declarative_base()

class Database:
    _engine = None
    _SessionLocal = None

    @staticmethod
    def initialize():
        if Database._engine is None:
            Database._engine = create_engine(Config.SUPABASE_URL)
            Database._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Database._engine)
        Base.metadata.create_all(bind=Database._engine)

    @staticmethod
    def get_session() -> Session:
        if Database._SessionLocal is None:
            raise RuntimeError("Database is not initialized. Call 'Database.initialize()' first.")
        return Database._SessionLocal()
