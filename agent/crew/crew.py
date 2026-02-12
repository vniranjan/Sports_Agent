"""Crew orchestration - runs the full pipeline."""
import sys
from pathlib import Path
from typing import Optional

import yaml

# Add backend to path for DB access
_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_root / "backend"))

from agent.crew.agents import (
    categorize_sport,
    extract_content,
    fetch_candidates_from_sources,
    summarize_with_llm,
)
from app.database import SessionLocal, init_db
from app.models import Article, Sport
from app.seed import seed_sports


def run_pipeline(sources_path: Optional[Path] = None) -> int:
    """Run full pipeline: fetch -> extract -> summarize -> save. Returns count saved."""
    if sources_path is None:
        sources_path = _root / "agent" / "config" / "sources.yaml"

    with open(sources_path) as f:
        sources_config = yaml.safe_load(f)

    if not sources_config:
        return 0

    candidates = fetch_candidates_from_sources(sources_config)
    articles_to_save = []
    seen_urls = set()

    for c in candidates:
        url = c.get("url")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        content = extract_content(url)
        if not content or len(content) < 50:
            continue

        headline = c.get("title", "No headline")
        summary = summarize_with_llm(content, headline)
        sport_slug = categorize_sport(headline, content, c.get("sport", "cricket"))

        articles_to_save.append({
            "headline": headline[:500],
            "summary": summary,
            "source_url": url[:2000],
            "source_name": c.get("source_name", "Unknown")[:200],
            "published_at": c.get("date"),
            "sport_slug": sport_slug,
        })

    # Persist to DB
    init_db()
    db = SessionLocal()
    seed_sports(db)
    db.commit()
    saved = 0
    try:
        sport_map = {s.slug: s.id for s in db.query(Sport).all()}
        for a in articles_to_save:
            sport_id = sport_map.get(a["sport_slug"])
            if not sport_id:
                continue
            existing = db.query(Article).filter_by(source_url=a["source_url"]).first()
            if existing:
                continue
            db.add(Article(
                sport_id=sport_id,
                headline=a["headline"],
                summary=a["summary"],
                source_url=a["source_url"],
                source_name=a["source_name"],
                published_at=a["published_at"],
            ))
            saved += 1
        db.commit()
    finally:
        db.close()

    return saved
