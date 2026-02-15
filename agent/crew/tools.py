"""Tools for RSS parsing and content extraction."""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup
from agents import function_tool


def parse_rss_feed(url: str, source_name: str, sport_slug: str) -> List[Dict]:
    """Parse RSS feed and return list of {title, url, date, source_name, sport}."""
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:15]:  # Limit per feed
            link = entry.get("link") or entry.get("href")
            if not link:
                continue
            # Parse date
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    pub_date = datetime(*entry.published_parsed[:6])
                except (TypeError, ValueError):
                    pass
            items.append({
                "title": entry.get("title", "").strip(),
                "url": link,
                "date": pub_date,
                "source_name": source_name,
                "sport": sport_slug,
            })
        return items
    except Exception:
        return []


def extract_article_content(url: str) -> Optional[str]:
    """Fetch URL and extract main article text."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; SportsNewsBot/1.0)",
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove script, style
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Prefer article, main, or common content containers
        for selector in ["article", "main", ".article-body", ".post-content", ".content", "#content"]:
            el = soup.select_one(selector)
            if el:
                text = el.get_text(separator=" ", strip=True)
                if len(text) > 100:
                    return _clean_text(text)

        # Fallback: body
        body = soup.find("body")
        if body:
            text = body.get_text(separator=" ", strip=True)
            return _clean_text(text)

        return _clean_text(soup.get_text())
    except Exception:
        return None


def _clean_text(text: str, max_len: int = 8000) -> str:
    """Clean and truncate text."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        text = text[:max_len] + "..."
    return text


# --- @function_tool wrappers for OpenAI Agents SDK ---

@function_tool
def fetch_rss_feeds() -> str:
    """Fetch articles from all RSS feeds configured in sources.yaml.

    Returns a JSON string of article candidates with title, url, date,
    source_name, and sport fields.
    """
    root = Path(__file__).resolve().parents[2]
    sources_yaml_path = root / "agent" / "config" / "sources.yaml"

    with open(sources_yaml_path) as f:
        sources_config = yaml.safe_load(f)

    candidates = []
    seen_urls: set[str] = set()
    for sport_slug, config in sources_config.items():
        for rss_source in config.get("rss", []):
            items = parse_rss_feed(rss_source["url"], rss_source["name"], sport_slug)
            for item in items:
                url = item.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    if item.get("date"):
                        item["date"] = item["date"].isoformat()
                    candidates.append(item)

    return json.dumps(candidates)
