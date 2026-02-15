"""Pipeline orchestration - runs agents sequentially using OpenAI Agents SDK."""
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from agents import Runner

# Add backend to path for DB access
_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_root / "backend"))

from agent.crew.agents import (
    categorization_agent,
    source_discovery_agent,
    summarization_agent,
)
from agent.crew.tools import extract_article_content
from app.database import SessionLocal, init_db
from app.models import Article, Sport
from app.seed import seed_sports

logger = logging.getLogger(__name__)


async def run_pipeline(sources_path: Optional[Path] = None) -> int:
    """Run full agent pipeline: discover -> extract -> summarize -> categorize -> save."""

    # Step 1: Source Discovery Agent
    logger.info("Step 1: Running Source Discovery Agent...")
    discovery_result = await Runner.run(
        source_discovery_agent,
        "Fetch all article candidates from the configured RSS feeds.",
    )
    candidates = discovery_result.final_output.candidates
    logger.info(f"  Discovered {len(candidates)} candidates")

    articles_to_save = []
    seen_urls: set[str] = set()

    # Steps 2-4: Process each candidate
    for i, candidate in enumerate(candidates):
        url = candidate.url
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        try:
            # Step 2: Content Extraction (plain function, no agent)
            content = extract_article_content(url)
            if not content or len(content) < 50:
                logger.debug(f"  Skipping {url}: insufficient content")
                continue

            headline = candidate.title or "No headline"

            # Step 3: Summarization Agent
            summary_result = await Runner.run(
                summarization_agent,
                f"Headline: {headline}\n\nArticle content:\n{content[:4000]}",
            )
            summarized = summary_result.final_output

            # Step 4: Categorization Agent
            cat_result = await Runner.run(
                categorization_agent,
                (
                    f"Headline: {summarized.headline}\n"
                    f"Summary: {summarized.summary}\n"
                    f"Candidate sport from RSS source: {candidate.sport}"
                ),
            )
            categorized = cat_result.final_output

            # Parse date string back to datetime for SQLAlchemy
            pub_date = None
            if candidate.date:
                try:
                    pub_date = datetime.fromisoformat(candidate.date)
                except (ValueError, TypeError):
                    pass

            articles_to_save.append({
                "headline": summarized.headline[:500],
                "summary": summarized.summary,
                "source_url": url[:2000],
                "source_name": candidate.source_name[:200],
                "published_at": pub_date,
                "sport_slug": categorized.sport_slug,
            })

            logger.info(
                f"  [{i+1}/{len(candidates)}] {summarized.headline[:60]}... "
                f"-> {categorized.sport_slug} ({categorized.confidence}: {categorized.reasoning})"
            )

        except Exception as e:
            logger.warning(f"  Failed processing {url}: {e}")
            continue

    # Step 5: Persist to DB
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

    logger.info(f"Pipeline complete. Saved {saved} new articles.")
    return saved


def run_pipeline_sync(sources_path: Optional[Path] = None) -> int:
    """Synchronous wrapper for scheduler compatibility."""
    return asyncio.run(run_pipeline(sources_path))
