"""FastAPI application entry point."""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load .env from project root
_root = Path(__file__).resolve().parents[2]
load_dotenv(_root / ".env")

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

from app.database import get_db, init_db
from app.seed import seed_sports
from app.scheduler import start_scheduler

app = FastAPI(title="Sports News API", version="0.1.0")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions and return 500."""
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.on_event("startup")
def startup():
    """Initialize database, seed sports, and start scheduler."""
    if os.getenv("TESTING"):
        return
    logger.info("Starting up...")
    init_db()
    db = next(get_db())
    try:
        seed_sports(db)
        db.commit()
    finally:
        db.close()
    start_scheduler()
    logger.info("Startup complete")


from app.api.sports import router as sports_router
from app.api.articles import router as articles_router

app.include_router(sports_router)
app.include_router(articles_router)
