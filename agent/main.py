"""Entry point for agent pipeline."""
import asyncio
import logging
import sys
from pathlib import Path

# Ensure project root is on path
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dotenv import load_dotenv
load_dotenv(_root / ".env")

# Configure logging so agent progress is visible
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)

from agent.crew.crew import run_pipeline


if __name__ == "__main__":
    saved = asyncio.run(run_pipeline())
    print(f"\nPipeline complete. Saved {saved} new articles.")
