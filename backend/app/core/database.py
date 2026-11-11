
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


# Create the SQLAlchemy database engine.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


# Create a reusable database session factory.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for all database models.
class Base(DeclarativeBase):
    pass


# Dependency for FastAPI database sessions.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
