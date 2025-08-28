from playwright.async_api import async_playwright
from scrapegraphai.graphs import SmartScraperGraph
from urllib.parse import urlparse
import os
from urllib.parse import urljoin
from prompts import LOAD_AND_SCRAPE_PROMPT

os.environ["OPENAI_API_KEY"] ="sk-proj.."

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 

GRAPH_CONFIG = {
    "llm": {
        "api_key": OPENAI_API_KEY,       
        "model": "gpt-4",   #openai/gpt-4o          
        # for Ollama add:
        # "format": "json",
        # "base_url": "http://localhost:11434",
        # "temperature": 0
    },
    "verbose": True,
    "headless": False,
}


def extract_description(detail_html):

    graph = SmartScraperGraph(
                prompt=LOAD_AND_SCRAPE_PROMPT,
                source=detail_html,
                config=GRAPH_CONFIG
            )

    result = graph.run()

    return result