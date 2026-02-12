"""Articles API endpoints."""
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Article, Sport
from app.schemas import ArticleWithSport

router = APIRouter(prefix="/api", tags=["articles"])


@router.get("/articles", response_model=List[ArticleWithSport])
def list_articles(
    db: Session = Depends(get_db),
    sport: Optional[str] = Query(None, description="Filter by sport slug"),
    from_date: Optional[date] = Query(None, alias="from"),
    to_date: Optional[date] = Query(None, alias="to"),
):
    """List articles with optional filters."""
    q = db.query(Article).options(joinedload(Article.sport)).join(Sport)
    if sport:
        q = q.filter(Sport.slug == sport)
    if from_date:
        q = q.filter(Article.published_at >= from_date)
    if to_date:
        end_of_day = datetime.combine(to_date, datetime.max.time())
        q = q.filter(Article.published_at <= end_of_day)
    return q.order_by(Article.published_at.desc().nullslast(), Article.created_at.desc()).all()


@router.get("/articles/{article_id}", response_model=ArticleWithSport)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get single article by ID."""
    article = db.query(Article).options(joinedload(Article.sport)).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
