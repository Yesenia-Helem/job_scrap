import asyncio
import sys
import json
from tools import get_page_html
from tools import get_page 

from llm_utils import get_llm_chain
#from extract_jobs import prompt_template


prompt_template = """
You are an expert web scraper.

Given the following HTML of a jobs listing page, identify:

- A CSS selector that matches all clickable job items.
- A CSS selector to extract the job title inside each job item.

Answer ONLY in JSON format like this:

{{
  "job_list_selector": "...",
  "title_selector": "...",
  "location_selector": "..."
}}

HTML:
{html}
"""


def get_job_selectors(html: str):
    llm_chain = get_llm_chain(prompt_template)
    response = llm_chain.run({"html": html[:6000]})
    try:
        selectors = json.loads(response)
    except json.JSONDecodeError:
        print("Failed to parse selectors JSON:")
        print(response)
        return None
    return selectors


def scrape_jobs_old(url: str):
    print(f"Scraping: {url}")
    html = get_page_html(url)
    
    llm_chain = get_llm_chain(prompt_template)
    
    text_content = html 
    result = llm_chain.run({"html": text_content})

    #result = llm_chain.run({"html": html[:6000]})
    try:
        jobs = json.loads(result)
    except json.JSONDecodeError:
        print("Failed to parse JSON. Raw output:")
        print(result)
        return []

    return jobs


async def scrape_jobs(url: str):
    page, html = await get_page(url)
    return {"html": html}



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    jobs = asyncio.run(scrape_jobs(url))

    print(json.dumps(jobs, indent=2, ensure_ascii=False))