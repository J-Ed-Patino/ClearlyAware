from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# Configure connection to the database
engine = create_engine(settings.database_url)

# Factory for creating new database sessions
SessionLocal = sessionmaker(bind=engine)

# Blueprint/base class for ORM models
class Base(DeclarativeBase):
    pass