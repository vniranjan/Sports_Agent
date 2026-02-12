"""Agent logic for research, extraction, summarization, and categorization."""
import os
from typing import Optional

from openai import OpenAI

from agent.crew.tools import extract_article_content, parse_rss_feed


def fetch_candidates_from_sources(sources_config: dict) -> list[dict]:
    """News Researcher: collect candidate articles from RSS sources."""
    candidates = []
    seen_urls = set()

    for sport_slug, config in sources_config.items():
        for rss_source in config.get("rss", []):
            items = parse_rss_feed(
                rss_source["url"],
                rss_source["name"],
                sport_slug,
            )
            for item in items:
                url = item.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    candidates.append(item)

    return candidates


def extract_content(url: str) -> Optional[str]:
    """Content Extractor: fetch and clean article text."""
    return extract_article_content(url)


def summarize_with_llm(content: str, headline: str) -> str:
    """Summarizer: generate 2-4 sentence summary via LLM."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return f"Summary unavailable (no API key). Key points from: {headline}"

    try:
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sports news summarizer. Produce 2-4 concise sentences highlighting the key takeaways. Be informative and avoid redundancy.",
                },
                {
                    "role": "user",
                    "content": f"Headline: {headline}\n\nArticle excerpt:\n{content[:4000]}",
                },
            ],
            max_tokens=200,
        )
        summary = resp.choices[0].message.content
        return summary.strip() if summary else headline
    except Exception:
        return headline


def categorize_sport(headline: str, content: str, candidate_sport: str) -> str:
    """Categorizer: confirm or correct sport (cricket vs soccer)."""
    text = (headline + " " + content).lower()
    if "cricket" in text or "cricinfo" in text or "cricbuzz" in text or "ipl" in text:
        return "cricket"
    if "football" in text or "soccer" in text or "premier league" in text or "fifa" in text:
        return "soccer"
    return candidate_sport
