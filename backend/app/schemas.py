"""Pydantic schemas for API."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SportBase(BaseModel):
    name: str
    slug: str


class SportResponse(SportBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ArticleBase(BaseModel):
    headline: str
    summary: str
    source_url: str
    source_name: str
    published_at: Optional[datetime] = None


class ArticleResponse(ArticleBase):
    id: int
    sport_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ArticleWithSport(ArticleResponse):
    sport: SportResponse
