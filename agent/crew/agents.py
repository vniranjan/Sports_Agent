"""Agent definitions for the sports news pipeline using OpenAI Agents SDK."""
from agents import Agent, ModelSettings

from agent.crew.models import (
    CategorizedArticle,
    DiscoveryResult,
    SummarizedArticle,
)
from agent.crew.tools import fetch_rss_feeds

_model = "gpt-4o-mini"

source_discovery_agent = Agent(
    name="Source Discovery Agent",
    instructions=(
        "You are a sports news source discovery agent. "
        "Use the fetch_rss_feeds tool to retrieve article candidates from configured RSS feeds. "
        "Parse the JSON result and return ALL candidates as a structured DiscoveryResult. "
        "Do not filter or remove any candidates."
    ),
    model=_model,
    model_settings=ModelSettings(temperature=0.2),
    tools=[fetch_rss_feeds],
    output_type=DiscoveryResult,
)

summarization_agent = Agent(
    name="Summarization Agent",
    instructions=(
        "You are a sports news summarizer. "
        "Given a headline and article content, produce a 2-4 sentence summary "
        "highlighting the key takeaways. Be concise, informative, and avoid redundancy. "
        "Return the result as a structured SummarizedArticle with the original headline "
        "and your generated summary."
    ),
    model=_model,
    model_settings=ModelSettings(temperature=0.3),
    tools=[],
    output_type=SummarizedArticle,
)

categorization_agent = Agent(
    name="Categorization Agent",
    instructions=(
        "You are a sports article categorization agent. "
        "Given a headline, summary, and candidate sport, determine the correct sport category. "
        "Valid sport slugs are: 'cricket', 'soccer'. "
        "Cricket articles discuss cricket, IPL, T20, test matches, "
        "wickets, batsmen, bowlers, innings, etc. "
        "Soccer articles discuss football, Premier League, "
        "FIFA, La Liga, Champions League, Serie A, Bundesliga, MLS, goals, penalties, etc. "
        "Analyze the content carefully and return your categorization "
        "with a confidence level (low/medium/high) and brief reasoning."
    ),
    model=_model,
    model_settings=ModelSettings(temperature=0.1),
    tools=[],
    output_type=CategorizedArticle,
)
