import asyncio
from bs4 import BeautifulSoup
from langchain_community.llms import Ollama
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.tools import HumanInputRun
from playwright.async_api import async_playwright

llm = Ollama(model="llama3")

def summarize_job_description(job_text: str) -> str:
    prompt = f"""
    Summarize this job description in no more than 3 lines:
    
    {job_text}
    """
    return llm.invoke(prompt)

summary_tool = Tool(
    name="JobSummaryTool",
    func=summarize_job_description,
    description="Summarizes job descriptions concisely."
)

agent = initialize_agent(
    tools=[summary_tool, HumanInputRun()],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

async def scrape_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://lcps.schoolspring.com/")

        print("Waiting for job listings to load...")
        try:
            await page.wait_for_selector(".job-list-item", timeout=10000)
        except Exception:
            print("No job listings appeared within 10 seconds.")
            await browser.close()
            return

        while True:
            try:
                load_more = await page.query_selector(".pds-secondary-btn")
                if load_more:
                    await load_more.click()
                    await page.wait_for_timeout(2000)
                else:
                    break
            except Exception:
                break

        jobs = await page.query_selector_all(".job-list-item")
        print(f"Total jobs found: {len(jobs)}")

        if not jobs:
            print("No jobs found")
            await browser.close()
            return

        for idx, job in enumerate(jobs, 1):
            print("Processing job..", idx)

            try:
                await job.scroll_into_view_if_needed()
                await job.click()
                await page.wait_for_selector(".job-details-container", timeout=10000)
                await page.wait_for_timeout(1000)

                container = await page.query_selector(".job-details-container")
                inner_html = await container.inner_html()

                soup = BeautifulSoup(inner_html, "html.parser")
                description = soup.get_text(separator="\n", strip=True)

                print(" Description job.")
                print(description[:300], "...\n") 
                agent.run(description)

                await page.go_back()
                await page.wait_for_timeout(1000)

            except Exception as e:
                print(f"Error processing job #{idx}: {e}")
                continue

        await browser.close()

if __name__ == "__main__":
    
    asyncio.run(scrape_jobs())