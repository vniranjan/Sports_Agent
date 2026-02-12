# Sports News Website

A sports news aggregator that collects top stories for **cricket** and **soccer** from global sources, with AI-generated summaries.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite/PostgreSQL
- **Frontend:** Next.js 14, Tailwind CSS
- **Agent:** Python pipeline (RSS, content extraction, OpenAI summarization)
- **Scheduler:** APScheduler (runs pipeline every 5 hours)

## Setup

1. **Copy environment file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your `OPENAI_API_KEY` (required for summaries).

2. **Backend**
   ```bash
   cd backend && python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Frontend**
   ```bash
   cd frontend && npm install
   ./scripts/sync-env.sh   # Copies NEXT_PUBLIC_* from root .env to frontend/.env.local
   ```

4. **Agent** (shares backend venv or install deps)
   ```bash
   pip install -r agent/requirements.txt
   ```

## Run

- **Backend:** `cd backend && uvicorn app.main:app --reload`
- **Frontend:** `cd frontend && npm run dev`
- **Agent pipeline** (manual): `python agent/main.py` (run from project root)

The backend starts a scheduler that runs the agent pipeline every 5 hours (configurable via `PIPELINE_INTERVAL_HOURS`). Set `DISABLE_SCHEDULER=1` to turn it off.

## Docker

```bash
docker compose up --build
```

Backend: http://localhost:8000  
Frontend: http://localhost:3000

Ensure `.env` exists with your API keys before running.

## Project Structure

- `agent/` - News pipeline: RSS fetch, content extraction, summarization, DB storage
- `backend/` - FastAPI API, SQLAlchemy models, scheduler
- `frontend/` - Next.js app, SportNav, ArticleCard, ArticleList
- `scripts/sync-env.sh` - Copies `NEXT_PUBLIC_*` from root `.env` to frontend
- `.env` - **Single source** for all secrets (root only; no sub-.env files)

## API

- `GET /health` - Health check
- `GET /api/sports` - List sports
- `GET /api/articles?sport=cricket&from=2026-02-01&to=2026-02-28` - List articles
- `GET /api/articles/{id}` - Get article

## Success Criteria

- 3+ RSS sources per sport
- Summaries 2-4 sentences
- Correct sport categorization
- Deduplication by source URL
- Scheduled runs every 4-6 hours
