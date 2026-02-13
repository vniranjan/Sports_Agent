# Sports News Website - Project Specification

## Project Overview

A sports news aggregator website that collects top news stories for **cricket** and **soccer** from global sources, organizes them by sport category, and presents headlines with AI-generated summaries of key takeaways.

## Tech Stack

- **Agent Pipeline:** Python (sequential pipeline with modular functions)
- **Backend:** FastAPI
- **Frontend:** Next.js
- **Database:** PostgreSQL (or SQLite for initial development)
- **Scheduling:** APScheduler (background job runner)
- **LLM:** OpenAI GPT-4o-mini (for article summarization)
- **Language:** Python 3.11+ (backend/agents), TypeScript (frontend)

## Sports Categories

1. **Cricket**
2. **Soccer** (Football)

## Core Features

### Phase 1: Agent Pipeline
- Sequential Python pipeline to search and assimilate news from multiple RSS sources
- Extract article content from URLs
- Generate concise summaries (key takeaways) using OpenAI LLM
- Categorize articles by sport (cricket/soccer) using rule-based classification
- Deduplicate stories by source URL
- Store structured data: sport, headline, summary, source URL, source name, published date

### Phase 2: Backend API
- RESTful API endpoints:
  - `GET /api/sports` - List available sports
  - `GET /api/articles` - List articles (with filters: sport, date range)
  - `GET /api/articles/{id}` - Get single article details
- Database models for sports and articles
- APScheduler background job to execute agent pipeline periodically (default: every 5 hours)

### Phase 3: Frontend
- Home page with sport category navigation
- Sport-specific pages showing:
  - Headline
  - AI-generated summary (key takeaways)
  - Source link
  - Publication date
- Responsive design
- Clean, modern UI

## Data Model

### Sports Table
- `id` (primary key)
- `name` (e.g., "Cricket", "Soccer")
- `slug` (e.g., "cricket", "soccer")
- `created_at`

### Articles Table
- `id` (primary key)
- `sport_id` (foreign key)
- `headline` (string)
- `summary` (text - AI-generated key takeaways)
- `source_url` (string, unique)
- `source_name` (string)
- `published_at` (datetime)
- `created_at` (datetime)
- `updated_at` (datetime)

## Agent Architecture

The agent pipeline is a sequential Python workflow composed of modular functions. Each stage processes data and passes results to the next.

### Pipeline Stages

1. **News Researcher** (`fetch_candidates_from_sources`)
   - Parses RSS feeds from configured sources
   - Collects candidate article URLs and metadata
   - Limits to 15 items per feed

2. **Content Extractor** (`extract_content`)
   - Fetches full article content from URLs
   - Cleans and normalizes text using BeautifulSoup
   - Truncates to 8000 characters

3. **Summarizer** (`summarize_with_llm`)
   - Generates 2-4 sentence summaries via OpenAI GPT-4o-mini
   - Highlights key takeaways

4. **Categorizer** (`categorize_sport`)
   - Rule-based sport classification using keyword matching
   - Handles edge cases where sport might be ambiguous

### Pipeline Orchestration (`run_pipeline`)
- Loads RSS source configuration from `sources.yaml`
- Executes stages sequentially: fetch → extract → summarize → categorize
- Deduplicates articles by `source_url`
- Persists results to database via SQLAlchemy

### Tools & Libraries
- `feedparser` - RSS feed parsing
- `beautifulsoup4` - Web scraping and content extraction
- `requests` - HTTP client
- `openai` - LLM API client for summarization

## News Sources

### Cricket
- ESPN Cricinfo RSS
- BBC Sport Cricket RSS
- Cricbuzz RSS

### Soccer
- ESPN Soccer RSS
- BBC Sport Football RSS

## Project Structure

```
sports-news-website/
├── agent/
│   ├── crew/
│   │   ├── agents.py          # Pipeline stage functions
│   │   ├── tools.py           # RSS parsing, content extraction utilities
│   │   └── crew.py            # Pipeline orchestration and DB persistence
│   ├── config/
│   │   └── sources.yaml       # RSS source configurations
│   └── main.py                # Entry point for agent pipeline
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app, CORS, startup events
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── database.py        # DB connection and initialization
│   │   ├── seed.py            # Database seeding (cricket, soccer)
│   │   ├── scheduler.py       # APScheduler background job runner
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── sports.py      # Sports endpoints
│   │       └── articles.py    # Articles endpoints
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/                   # Next.js app directory
│   │   ├── layout.tsx
│   │   ├── page.tsx           # Home page
│   │   └── [sport]/
│   │       └── page.tsx       # Sport-specific page
│   ├── components/
│   │   ├── SportNav.tsx
│   │   ├── ArticleCard.tsx
│   │   └── ArticleList.tsx
│   ├── lib/
│   │   └── api.ts             # API client functions
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
├── scripts/
│   └── sync-env.sh            # Copies NEXT_PUBLIC_* vars to frontend/.env.local
├── .env.example
├── .gitignore
├── README.md
├── SPECIFICATION.md            # This file
└── docker-compose.yml
```

## Environment Variables

### Backend/Agent
- `DATABASE_URL` - Database connection string (defaults to SQLite)
- `OPENAI_API_KEY` - OpenAI API key (required for summarization)
- `LOG_LEVEL` - Logging level (default: INFO)
- `PIPELINE_INTERVAL_HOURS` - Agent pipeline run interval (default: 5)
- `DISABLE_SCHEDULER` - Set to disable background scheduling

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

## Implementation Phases

### Phase 1: Foundation
- [x] Set up project structure
- [x] Initialize database with sports table (cricket, soccer)
- [x] Create FastAPI app with health check
- [x] Set up agent pipeline structure

### Phase 2: Agent Pipeline
- [x] Implement news researcher with RSS tools
- [x] Implement content extractor
- [x] Implement LLM summarizer
- [x] Create pipeline orchestration
- [x] Test end-to-end: sources → articles → summaries → DB

### Phase 3: Backend API
- [x] Create article database models
- [x] Implement `/api/sports` endpoint
- [x] Implement `/api/articles` endpoint with filters
- [x] Add deduplication logic
- [x] Set up APScheduler background job runner

### Phase 4: Frontend
- [x] Set up Next.js project
- [x] Create home page with sport navigation
- [x] Create sport-specific article listing pages
- [x] Implement API client
- [x] Add responsive styling with Tailwind CSS

### Phase 5: Polish & Deploy
- [x] Error handling and logging
- [x] Docker and Docker Compose setup
- [ ] Caching strategy
- [ ] Performance optimization

## Success Criteria

- Agent pipeline successfully fetches and processes news from at least 3 sources per sport
- Summaries are concise (2-4 sentences) and capture key takeaways
- Articles are correctly categorized by sport
- Frontend displays articles organized by sport with clean UI
- System runs automatically on schedule (every 5 hours)
- No duplicate articles shown to users

## Future Enhancements (Post-MVP)

- News API integration for broader source coverage
- Add more sports categories
- User preferences/favorites
- Search functionality
- Article detail pages
- Email/newsletter digest
- Real-time updates via WebSockets
- Mobile app

---

**Created:** February 10, 2026
**Last Updated:** February 12, 2026
