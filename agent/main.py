"""Entry point for agent pipeline."""
import sys
from pathlib import Path

# Ensure project root is on path
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dotenv import load_dotenv
load_dotenv(_root / ".env")

from agent.crew.crew import run_pipeline


if __name__ == "__main__":
    saved = run_pipeline()
    print(f"Pipeline complete. Saved {saved} new articles.")
