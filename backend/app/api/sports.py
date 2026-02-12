"""Sports API endpoints."""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Sport
from app.schemas import SportResponse

router = APIRouter(prefix="/api", tags=["sports"])


@router.get("/sports", response_model=List[SportResponse])
def list_sports(db: Session = Depends(get_db)):
    """List all available sports."""
    return db.query(Sport).order_by(Sport.id).all()
