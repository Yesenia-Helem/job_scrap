from playwright_tools import create_playwright_browser_tools
from agent2 import create_agent
from save_utils import save_to_json

def main():
    tools = create_playwright_browser_tools()
    agent = create_agent(tools)

    prompt = (
        "Go to https://lcps.schoolspring.com. "
        "Click the button that says 'More jobs' to load more jobs. "
        "After loading more jobs, click on each individual job listing, extract the title, location, and full description. "
        "Return all jobs as a JSON array with keys: title, location, description. "
        "Then navigate back to continue with the next job."
    )

    result = agent.run(prompt)

    print("Raw output:", result)

    try:
        import json
        jobs = json.loads(result)
    except Exception as e:
        print(f"Could not parse JSON: {e}")
        jobs = [{"raw": result}]

    save_to_json(jobs)

if __name__ == "__main__":
    main()
