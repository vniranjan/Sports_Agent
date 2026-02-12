"""Database seeding script."""
from app.models import Sport


def seed_sports(session):
    """Seed sports table with cricket and soccer."""
    sports = [
        Sport(name="Cricket", slug="cricket"),
        Sport(name="Soccer", slug="soccer"),
    ]
    for sport in sports:
        existing = session.query(Sport).filter_by(slug=sport.slug).first()
        if not existing:
            session.add(sport)
