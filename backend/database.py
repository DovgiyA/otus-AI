"""
Database configuration and session management using SQLAlchemy.
Supports both PostgreSQL and SQLite with automatic schema creation.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings
import os

# Detect database type
is_sqlite = "sqlite" in settings.DATABASE_URL

# Create engine with appropriate connection parameters
engine_kwargs = {}
if is_sqlite:
    # For SQLite, add check_same_thread=False for development
    engine_kwargs = {"connect_args": {"check_same_thread": False}}
    # Create data directory if using SQLite with file path
    if "sqlite:///" in settings.DATABASE_URL and not ":memory:" in settings.DATABASE_URL:
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
else:
    # For PostgreSQL
    engine_kwargs = {}

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL logging
    **engine_kwargs
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session in FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables and seed initial data."""
    Base.metadata.create_all(bind=engine)
    db_type = "PostgreSQL" if not is_sqlite else "SQLite"
    print(f"✓ Database ({db_type}) tables created successfully")
