"""APScheduler job to run agent pipeline periodically."""
import os
import sys
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

# Add project root for agent imports
_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
if str(_root / "backend") not in sys.path:
    sys.path.insert(0, str(_root / "backend"))


def run_agent_pipeline():
    """Job: run the agent pipeline."""
    try:
        from agent.crew.crew import run_pipeline_sync
        saved = run_pipeline_sync()
        print(f"Scheduled pipeline: saved {saved} articles")
    except Exception as e:
        print(f"Scheduled pipeline error: {e}")


def start_scheduler():
    """Start background scheduler for agent pipeline."""
    if os.getenv("TESTING") or os.getenv("DISABLE_SCHEDULER"):
        return None
    interval_hours = int(os.getenv("PIPELINE_INTERVAL_HOURS", "5"))
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_agent_pipeline, "interval", hours=interval_hours)
    scheduler.start()
    return scheduler
