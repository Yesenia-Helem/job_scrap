import csv
import json
import re
from datetime import datetime, timedelta
import os

def init_jobs_csv(jobsite: str) -> str:

    csv_filename = f"jobs_{jobsite}_mvdc.csv"

    if not os.path.exists(csv_filename):
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = [
                "job_title", "company", "company_id", "job_id", "city", "state",
                "salary", "posted_date", "job_url", "education_needed",
                "is_remote", "ended_at", "last_scanned_at", "description_summary"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    return csv_filename


def save_job_to_csv(csv_filename: str, job_data: dict):
    
    fieldnames = [
        "job_title", "company", "company_id", "job_id", "city", "state",
        "salary", "posted_date", "job_url", "education_needed",
        "is_remote", "ended_at", "last_scanned_at", "description"
    ]

    with open(csv_filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(job_data)

    print(job_data)
    print("====================================================")


def normalize_job_data(result):
    """
    Normalize the scraper output to get a job data dict.
    Handles cases where result can be dict, list, JSON string, etc.
    """

    if isinstance(result, str):
        try:
            result = json.loads(result)
        except Exception:
            print("Warning: Could not parse JSON from string:", result)
            return None

    if isinstance(result, list):
        
        if len(result) == 0:
            return None
        if isinstance(result[0], dict):
            return result[0]
        return None

    if isinstance(result, dict):
        if "content" in result:
            return result["content"]
        return result
    return None

def safe_parse_json(raw):
    """Try to clean and parse a malformed JSON string with extra braces."""
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        return None
    
    cleaned = re.sub(r'^\s*\{\{', '{', raw)
    cleaned = re.sub(r'\}\}\s*$', '}', cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("Could not parse JSON:", e)
        return None
    
def normalize_job_data(result):
    """
    Normalize the scraper output and return a single job dict (first job) or None.
    Handles:
      - result as JSON string (dict or list)
      - result as dict with 'content' that can be a string, dict, or list
      - result as list of dicts
      - result as plain dict
    """
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except Exception as e:
            print("Warning: could not parse top-level JSON string:", e)
            return None

    if isinstance(result, dict) and "content" in result:
        content = result["content"]

        if isinstance(content, str):
            try:
                content_parsed = json.loads(content)
            except Exception as e:
                print("Warning: could not parse JSON inside 'content':", e)
                return None
        else:
            content_parsed = content

        if isinstance(content_parsed, dict):
            return content_parsed
        if isinstance(content_parsed, list) and len(content_parsed) > 0 and isinstance(content_parsed[0], dict):
            return content_parsed[0]
        return None

    if isinstance(result, list):
        if len(result) == 0:
            return None
        if isinstance(result[0], dict):
            return result[0]
        return None

    if isinstance(result, dict):
        return result

    return None




def parse_relative_date(relative_text):
    """
    Converst text like '2 Days Ago' to YYYY-MM-DD
    """
    today = datetime.today()
    
    relative_text = relative_text.lower().strip()
    
    match = re.match(r'(\d+)\s+(day|week|month|year)s?\s+ago', relative_text)
    
    if match:
        value, unit = int(match.group(1)), match.group(2)
        
        if unit == "day":
            date_obj = today - timedelta(days=value)
        elif unit == "week":
            date_obj = today - timedelta(weeks=value)
        elif unit == "month":
            date_obj = today - timedelta(days=value*30)
        elif unit == "year":
            date_obj = today - timedelta(days=value*365)
        
        return date_obj.strftime("%Y-%m-%d")
    

