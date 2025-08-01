import sys
import json
from tools import get_page_html, get_page
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


def scrape_jobs(url: str):
    page, html = get_page(url)  
    
    print('after get page in scrape jobs')
    
    selectors = get_job_selectors(html)
    if selectors is None:
        print("Could not get selectors, aborting")
        return []

    job_list_selector = selectors["job_list_selector"]
    title_selector = selectors["title_selector"]
    location_selector = selectors["location_selector"]

    job_cards = page.locator(job_list_selector)

    count = job_cards.count()
    print(f"Found {count} jobs, extracting details...")

    jobs = []
    for i in range(count):
        job = job_cards.nth(i)
        job.click()
        page.wait_for_timeout(1500)  
        detail_html = page.content()
        
        title = job.locator(title_selector).inner_text()
        location = job.locator(location_selector).inner_text()

        jobs.append({
            "title": title,
            "location": location,
            "detail_html": detail_html 
        })

    #page.context.browser.close()
    return jobs



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    jobs = scrape_jobs(url)
    print(json.dumps(jobs, indent=2, ensure_ascii=False))
