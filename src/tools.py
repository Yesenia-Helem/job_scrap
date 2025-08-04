import asyncio
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# for langchain
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM


#with Qdrant
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant

import time
from tqdm import tqdm
import csv
import shutil
import os
import json
from uuid import uuid4
from datetime import datetime



def qacontext(retriever_, question, llm):
    retrieved_docs = retriever_.invoke(question)
    context = ' '.join([doc.page_content for doc in retrieved_docs])

    response = llm.invoke(f"""Answer the question according to the context given very briefly:
                Question: {question}.
                Context: {context}
    """)
    
    return response


today_str = datetime.today().strftime("%Y-%m-%d")

prompt_template = f"""
Assume today's date is {today_str}.

From the following job posting text, extract only the exact **publication date** in YYYY-MM-DD format.

If the text uses relative expressions like "today", "yesterday", or "X days ago", calculate the exact date accordingly.

If no such information is found, return only: unknown

Do not include any explanation, text, or extra content—just the final date string.
"""

prompt_template_title = """
Extract only the **full job title** from the following posting text.

- Do **not** summarize or shorten the title.
- Do **not** include explanations, locations, company names, or sentence fragments. Return only the exact title string, exactly as it appears in the posting.
"""
# Return only the exact title string, exactly as it appears in the posting.

prompt_summary_template = """
Read the following job posting text and provide a concise summary of the job description.  
Return only the summary in a few sentences, without adding any extra commentary or unrelated information.
"""


question_dict = {
    "salary": "What is the salary for this job? Please answer only with the salary amount and unit, like '$10 per hour'.",
    "title": prompt_template_title,
    "location": "Return only the city and state** where this job is located. No full sentences, no extra explanation. Just the raw location.",
    "postedAt": prompt_template,
    "description":prompt_summary_template
    }

#"title":   "What is the posted job position? ", 
# location: "Where is this job position located? Please include city and state."
#"title": "Return only the job title from the following posting. Do not add any explanation, location, or full sentence. Just the raw title.",
#postedAt: #"When was this job posting published? "


def get_page_html(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        print(f"Visiting {url}")
        page.goto(url, timeout=60000)

        try:
            page.wait_for_selector("body", timeout=15000)
            page.mouse.wheel(0, 3000)  
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"No content: {e}")

        text = page.inner_text("body")

        with open("debug_output.txt", "w") as f:
            f.write(text)

        browser.close()
        return text

#def get_job_description()


def get_page_old_s(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        print(f"Visiting {url}")
        page.goto(url, timeout=60000)

        try:
            page.wait_for_selector("body", timeout=15000)
        except Exception as e:
            print(f"There is no content: {e}")

        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(2000)


        for i in range(10):
            try:
                load_more_button = page.locator("button:has-text('More jobs')")
                if load_more_button.is_visible():
                    print(f"Clic #{i+1} en 'More jobs'")
                    load_more_button.click()
                    page.wait_for_timeout(3000)
                    #page.mouse.wheel(0, 2000)
                else:
                    break
            except Exception as e:
                print(f"Error - click : {e}")
                break

        text = page.inner_text("body")
        
        jobs = page.locator(".job-list-item")
        total = jobs.count()
        print(f"Total jobs found just jobs: {total}")

        if total == 0:
            print("No jobs found.")
            browser.close()
            return []

        job_data = []

        csv_file = "jobs_output.csv"
        fieldnames = ["title", "salary", "location", "postedAt", "description"]
        write_header = not os.path.exists(csv_file)


        for idx in range(total):
            print(f"\nProcessing job #{idx+1}...")
            try:
                job = jobs.nth(idx)
                job.scroll_into_view_if_needed()
                job.click()

                #container = page.locator(".job-details-container")
    
                page.wait_for_selector("#jobDetails-desktop:visible", timeout=20000)

                container = page.locator("#jobDetails-desktop")
                                
                description = container.inner_text()
                
                print('======== Description ==========')
                print(description)
                print('======== Description ==========')
                
                
                # LLM PIPELINE
                docs = [Document(page_content=description)]

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1200, chunk_overlap=120, add_start_index=True
                )
                all_splits = text_splitter.split_documents(docs)

                print(f"Nro chunks generated: {len(all_splits)}")

                # LLM and Embeddings
                llm = OllamaLLM(model="llama3.2:1b")
                local_embeddings = OllamaEmbeddings(model="all-minilm")

                collection_name = f"job_{idx}"
                vectorstore = Qdrant.from_documents(
                    all_splits,
                    embedding=local_embeddings,
                    location=":memory:",
                    collection_name=collection_name
                )

                retriever = vectorstore.as_retriever()

                # questions for LLM
                salary = qacontext(retriever, question_dict["salary"], llm)
                title = qacontext(retriever, question_dict["title"], llm)
                location = qacontext(retriever, question_dict["location"], llm)
                postedAt = qacontext(retriever, question_dict["postedAt"], llm)
                description_job = qacontext(retriever, question_dict["description"], llm)

                print("Extracted info:")
                print("Title:", title)
                print("Salary:", salary)
                print("Location:", location)
                print("Posted At:", postedAt)

                with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    if write_header:
                        writer.writeheader()
                        write_header = False  # Solo la primera vez
                    writer.writerow({
                        "title": title,
                        "salary": salary,
                        "location": location,
                        "postedAt": postedAt,
                        "description": description_job
                    })


                page.go_back()
                page.wait_for_timeout(1000)


            except Exception as e:
                print(f"Error processing job #{idx+1}: {e}")
                continue

        html = page.content()  
        
        
        with open("debug_output.txt", "w") as f:
            f.write(text)

        with open("debug_full_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        return page, html
    


async def get_page(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        print(f"Visiting {url}")
        await page.goto(url, timeout=60000)

        try:
            await page.wait_for_selector("body", timeout=15000)
        except Exception as e:
            print(f"There is no content: {e}")

        await page.mouse.wheel(0, 2000)
        await page.wait_for_timeout(2000)

        for i in range(10):
            try:
                load_more_button = page.locator("button:has-text('More jobs')")
                if await load_more_button.is_visible():
                    print(f"Clic #{i+1} en 'More jobs'")
                    await load_more_button.click()
                    await page.wait_for_timeout(3000)
                else:
                    break
            except Exception as e:
                print(f"Error - click : {e}")
                break

        text = await page.inner_text("body")

        jobs = page.locator(".job-list-item")
        total = await jobs.count()
        print(f"Total jobs found just jobs: {total}")

        if total == 0:
            print("No jobs found.")
            await browser.close()
            return None, None

        job_data = []

        csv_file = "jobs_output.csv"
        fieldnames = ["title", "salary", "location", "postedAt", "description"]
        write_header = not os.path.exists(csv_file)

        for idx in range(total):
            print(f"\nProcessing job #{idx+1}...")
            try:
                job = jobs.nth(idx)
                await job.scroll_into_view_if_needed()
                await job.click()

                await page.wait_for_selector("#jobDetails-desktop:visible", timeout=20000)

                container = page.locator("#jobDetails-desktop")

                description = await container.inner_text()
                print('======== Description ==========')
                print(description)
                print('======== Description ==========')

                # LLM PIPELINE
                docs = [Document(page_content=description)]

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1200, chunk_overlap=120, add_start_index=True
                )
                all_splits = text_splitter.split_documents(docs)

                print(f"Nro chunks generated: {len(all_splits)}")

                llm = OllamaLLM(model="llama3.2:1b")
                local_embeddings = OllamaEmbeddings(model="all-minilm")

                collection_name = f"job_{idx}"
                vectorstore = Qdrant.from_documents(
                    all_splits,
                    embedding=local_embeddings,
                    location=":memory:",
                    collection_name=collection_name
                )

                retriever = vectorstore.as_retriever()

                salary = qacontext(retriever, question_dict["salary"], llm)
                title = qacontext(retriever, question_dict["title"], llm)
                location = qacontext(retriever, question_dict["location"], llm)
                postedAt = qacontext(retriever, question_dict["postedAt"], llm)
                description_job = qacontext(retriever, question_dict["description"], llm)

                print("Extracted info:")
                print("Title:", title)
                print("Salary:", salary)
                print("Location:", location)
                print("Posted At:", postedAt)

                with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    if write_header:
                        writer.writeheader()
                        write_header = False
                    writer.writerow({
                        "title": title,
                        "salary": salary,
                        "location": location,
                        "postedAt": postedAt,
                        "description": description_job
                    })

                #await page.go_back()
                #await page.wait_for_timeout(1000)

            except Exception as e:
                print(f"Error processing job #{idx+1}: {e}")
                continue

        html = await page.content()

        with open("debug_output.txt", "w", encoding="utf-8") as f:
            f.write(text)

        with open("debug_full_page.html", "w", encoding="utf-8") as f:
            f.write(html)

        await browser.close()
        return page, html