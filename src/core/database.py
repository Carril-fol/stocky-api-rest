from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from .settings import Config

load_dotenv()

class Base(DeclarativeBase):
    pass

class Database:
    _engine: Engine = None
    _SessionLocal: sessionmaker[Session] = None

    @classmethod
    def initialize(cls, create_tables: bool = False):
        if cls._engine is not None:
            return

        cls._engine = create_engine(
            Config.NEON_DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_size=5,
            max_overflow=10,
            future=True,
        )
        cls._SessionLocal = sessionmaker(
            bind=cls._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=Session,
        )

        if create_tables:
            Base.metadata.create_all(bind=cls._engine)

    @staticmethod
    @contextmanager
    def session():
        if Database._SessionLocal is None:
            raise RuntimeError("Database is not initialized. Call 'Database.initialize()' first.")

        session = Database._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_session() -> Session:
        if Database._SessionLocal is None:
            raise RuntimeError("Database is not initialized. Call 'Database.initialize()' first.")

        return Database._SessionLocal()
