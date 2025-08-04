

Automatically detects relevant HTML structure using a language model

Workflow Overview

1. Load the target job website.
2. Collect all job links.
3. Visit each job and extract:
   - Job title
   - Job location
   - Full job description
4. Save results in JSON.

Example:

## How to Run

```bash
python3 src/agent.py "https://lcps.schoolspring.com/"
```


Workflow

![Job Scraping Workflow](src/flowchart.png)
