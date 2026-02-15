"""Pydantic models for structured inter-agent data exchange."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ArticleCandidate(BaseModel):
    """A candidate article discovered from an RSS feed."""
    title: str
    url: str
    date: Optional[str] = None
    source_name: str
    sport: str


class DiscoveryResult(BaseModel):
    """Output of the Source Discovery Agent."""
    candidates: list[ArticleCandidate]


class SummarizedArticle(BaseModel):
    """Output of the Summarization Agent."""
    headline: str
    summary: str


class CategorizedArticle(BaseModel):
    """Output of the Categorization Agent."""
    sport_slug: str = Field(description="Either 'cricket' or 'soccer'")
    confidence: str = Field(description="low, medium, or high")
    reasoning: str = Field(description="Brief explanation for the categorization")
