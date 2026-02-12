# Sports News Website - Project Specification

## Project Overview

A sports news aggregator website that collects top news stories for **cricket** and **soccer** from global sources, organizes them by sport category, and presents headlines with AI-generated summaries of key takeaways.

## Tech Stack

- **Agent Framework:** CrewAI
- **Backend:** FastAPI
- **Frontend:** Next.js
- **Database:** PostgreSQL (or SQLite for initial development)
- **Language:** Python 3.11+ (backend/agents), TypeScript (frontend)

## Sports Categories

1. **Cricket**
2. **Soccer** (Football)

## Core Features

### Phase 1: Agent Pipeline
- CrewAI agents to search and assimilate news from multiple sources
- Extract article content from URLs
- Generate concise summaries (key takeaways) using LLM
- Categorize articles by sport (cricket/soccer)
- Deduplicate stories from multiple sources
- Store structured data: sport, headline, summary, source URL, source name, published date

### Phase 2: Backend API
- RESTful API endpoints:
  - `GET /api/sports` - List available sports
  - `GET /api/articles` - List articles (with filters: sport, date range)
  - `GET /api/articles/{id}` - Get single article details
- Database models for sports and articles
- Scheduled job runner (cron/Celery) to execute agent pipeline periodically

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
- `source_url` (string)
- `source_name` (string)
- `published_at` (datetime)
- `created_at` (datetime)
- `updated_at` (datetime)

## Agent Architecture (CrewAI)

### Agent Roles

1. **News Researcher Agent**
   - Searches for news articles from configured sources
   - Filters by sport category and relevance
   - Returns candidate URLs and metadata

2. **Content Extractor Agent**
   - Fetches full article content from URLs
   - Cleans and normalizes text
   - Handles different source formats

3. **Summarizer Agent**
   - Analyzes article content
   - Generates concise summaries highlighting key takeaways
   - Ensures summaries are informative and non-redundant

4. **Categorizer Agent** (optional, can be rule-based)
   - Confirms sport category assignment
   - Handles edge cases where sport might be ambiguous

### Tools Required
- RSS feed parser
- Web scraping/content extraction (e.g., `readability-lxml`, `newspaper3k`)
- News API clients (e.g., News API, GNews)
- LLM API client (OpenAI, Anthropic, or local model)

## News Sources

### Cricket
- ESPN Cricinfo RSS
- BBC Sport Cricket RSS
- Cricbuzz RSS
- News API searches for "cricket"

### Soccer
- ESPN Soccer RSS
- BBC Sport Football RSS
- The Athletic RSS (if available)
- News API searches for "soccer" OR "football"

## Project Structure

```
sports-news-website/
├── agent/
│   ├── crew/
│   │   ├── agents.py          # CrewAI agent definitions
│   │   ├── tasks.py            # Task definitions
│   │   ├── tools.py            # Custom tools (RSS, scraping, etc.)
│   │   └── crew.py             # Crew orchestration
│   ├── config/
│   │   └── sources.yaml        # News source configurations
│   └── main.py                 # Entry point for agent pipeline
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── database.py         # DB connection
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── sports.py       # Sports endpoints
│   │       └── articles.py     # Articles endpoints
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/                    # Next.js app directory
│   │   ├── layout.tsx
│   │   ├── page.tsx            # Home page
│   │   ├── [sport]/
│   │   │   └── page.tsx        # Sport-specific page
│   │   └── api/                # API route handlers (if needed)
│   ├── components/
│   │   ├── SportNav.tsx
│   │   ├── ArticleCard.tsx
│   │   └── ArticleList.tsx
│   ├── lib/
│   │   └── api.ts              # API client functions
│   ├── package.json
│   └── tsconfig.json
├── .gitignore
├── README.md
├── SPECIFICATION.md            # This file
└── docker-compose.yml          # Optional: for local dev setup
```

## Environment Variables

### Backend/Agent
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY`) - LLM API key
- `NEWS_API_KEY` - News API key (if using News API)
- `LOG_LEVEL` - Logging level

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Set up project structure
- [ ] Initialize database with sports table (cricket, soccer)
- [ ] Create basic FastAPI app with health check
- [ ] Set up CrewAI environment and basic agent structure

### Phase 2: Agent Pipeline (Week 2)
- [ ] Implement News Researcher Agent with RSS/API tools
- [ ] Implement Content Extractor Agent
- [ ] Implement Summarizer Agent
- [ ] Create Crew orchestration
- [ ] Test end-to-end: one sport → articles → summaries → DB

### Phase 3: Backend API (Week 3)
- [ ] Create article database models
- [ ] Implement `/api/sports` endpoint
- [ ] Implement `/api/articles` endpoint with filters
- [ ] Add deduplication logic
- [ ] Set up scheduled job runner (cron or Celery)

### Phase 4: Frontend (Week 4)
- [ ] Set up Next.js project
- [ ] Create home page with sport navigation
- [ ] Create sport-specific article listing pages
- [ ] Implement API client
- [ ] Add responsive styling

### Phase 5: Polish & Deploy (Week 5)
- [ ] Error handling and logging
- [ ] Caching strategy
- [ ] Performance optimization
- [ ] Deployment setup (Docker, cloud platform)

## Success Criteria

- Agent pipeline successfully fetches and processes news from at least 3 sources per sport
- Summaries are concise (2-4 sentences) and capture key takeaways
- Articles are correctly categorized by sport
- Frontend displays articles organized by sport with clean UI
- System runs automatically on schedule (every 4-6 hours)
- No duplicate articles shown to users

## Future Enhancements (Post-MVP)

- Add more sports categories
- User preferences/favorites
- Search functionality
- Article detail pages
- Email/newsletter digest
- Real-time updates via WebSockets
- Mobile app

---

**Created:** February 10, 2026  
**Last Updated:** February 10, 2026
