from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

graph_config = {
   "llm": {
      "model": "ollama/mistral",
      "temperature": 1,
      "format": "json", 
      "model_tokens": 2000, 
      "base_url": "http://localhost:11434", 
   }
}

prompt_template = "Extract all visible job postings from the page. For each job, return a JSON object with the following keys: 'title', 'location', and 'description'. Return the output as a JSON array. Make sure the JSON is valid and contains all the data available from the page."


prompt=(
      "Go to the website and extract a 3 job postings with their description. "
      "For each job, include the job title, location, and full description if available. To obtain "
      "Return the information in a structured JSON array, with each object containing "
      "'title', 'location', and 'description'."
   ),

prompt = (
    "Go to the website https://jobs.pwcs.edu/. "
    "Then, for the first 3 job postings, click on each job title to open the popup window. "
    "In each popup, extract the job title, location, and full job description. "
    "Return the results as a JSON array with 3 objects, each containing the keys: 'title', 'location', and 'description'."
)


smart_scraper_graph = SmartScraperGraph(
   prompt = (
    "Go to the website https://jobs.pwcs.edu/. "
    "Then, for the first 3 job postings, click on each job title to open the popup window. "
    "In each popup, extract the job title, location, and full job description. "
    "Return the results as a JSON array with 3 objects, each containing the keys: 'title', 'location', and 'description'."
    ),
   source="https://jobs.pwcs.edu/",
   config=graph_config
)

result = smart_scraper_graph.run()
print(result)