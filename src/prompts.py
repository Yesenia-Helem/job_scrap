
LOAD_AND_SCRAPE_PROMPT = """
For each job click or open it to view details, and extract in JSON:
- job_title
- job_id
- location (city and state)
- salary
- posted_date: where the job were posted
- description (1-7 sentences).
Return only JSON.
"""

# e.g., "$72,758 - $130,041" or "$20/hour", otherwise "NA".

LOAD_AND_SCRAPE_PROMPT = """
You are given the full HTML content of a job posting.
Extract the following fields in JSON:

- job_title
- job_id
- location (city and state)
- salary: extract any salary mentioned, including ranges (e.g. "$20/hour" or "$50,000 - $80,000/year"). 
  If the salary is mentioned as a hiring range in text like "This position has a hiring range of $18.33 - $31.61", extract it in the same format.
- education_needed: extract the minimum education or qualifications required (e.g., "Bachelor's degree in Computer Science", "High school diploma", "Master's preferred", etc).
- description: 3-7 sentence summary of the job.

Return only valid JSON.
"""

LOAD_AND_SCRAPE_PROMPT = """
You are given the full HTML content of a job posting.
Extract the following fields in JSON:

- job_title
- job_id
- city: extract all cities mentioned for the job location. 
  If multiple cities are listed, separate them with commas (e.g., "Richmond, Arlington").
- state: extract the corresponding state(s) or region(s).
  If there are multiple cities with different states, list the city–state pairs instead (e.g., "Richmond, VA; Washington, DC").
- salary: extract any salary mentioned, including ranges (e.g. "$20/hour" or "$50,000 - $80,000/year"). 
- education_needed: extract ONLY the minimum required education level (e.g., "High school diploma", "Bachelor's degree", "Master's degree", "PhD"). Do NOT include majors, coursework, experience, or skills — only the education level.
- is_remote: return true if the posting explicitly says remote, hybrid, telecommute, or work-from-home; otherwise return false.
- posted_date: where the job were posted
- description: 3-7 sentence summary of the job.


Return only valid JSON.
"""
