"""Database connection and session management."""
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load .env from project root
_root = Path(__file__).resolve().parents[2]
load_dotenv(_root / ".env")

import os

_db_path = (_root / "sports_news.db").resolve()
_default_db = f"sqlite:///{_db_path}"
DATABASE_URL = os.getenv("DATABASE_URL", _default_db)
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    from app.models import Base as ModelsBase
    ModelsBase.metadata.create_all(bind=engine)
