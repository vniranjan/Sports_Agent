"""SQLAlchemy models for sports and articles."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Sport(Base):
    """Sport category model."""

    __tablename__ = "sports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship("Article", back_populates="sport")


class Article(Base):
    """Article model."""

    __tablename__ = "articles"
    __table_args__ = (UniqueConstraint("source_url", name="uq_article_source_url"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False, index=True)
    headline = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    source_url = Column(String(2000), nullable=False)
    source_name = Column(String(200), nullable=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sport = relationship("Sport", back_populates="articles")
