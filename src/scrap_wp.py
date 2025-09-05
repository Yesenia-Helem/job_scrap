import asyncio
from playwright.async_api import async_playwright
from scrapegraphai.graphs import SmartScraperGraph
from urllib.parse import urlparse
import os
from urllib.parse import urljoin
import csv
import json
import re
from norm_data import normalize_job_data, safe_parse_json, parse_relative_date, init_jobs_csv, save_job_to_csv
from llm_model import extract_description
import pandas as pd
from datetime import datetime
import jobnames 



async def scrape_lcps(url: str, max_jobs=10):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("body")

        while True:
            try:
                load_more = await page.query_selector("text=/load more|more jobs|next/i")
                if load_more:
                    print("Clicking 'Load more'…")
                    await load_more.click()
                    await page.wait_for_timeout(2000)
                else:
                    break
            except:
                break


        jobs = page.locator(".job-list-item")
        count = await jobs.count()
        print(f"Found {count} jobs.")

        results = []
        for i in range(min(max_jobs, count)):
            try:
                print(f"\nProcessing job #{i+1}")
                job = jobs.nth(i)
                await job.scroll_into_view_if_needed()
                await job.click()
                await page.wait_for_timeout(2000)

                detail_html = await page.content()

                result = extract_description(detail_html)
                results.append(result)

                #await page.go_back()
                #await page.wait_for_timeout(1000)
            except Exception as e:
                print("Error:", e)
                continue

        await browser.close()
        return results
    

async def scrape_mcdean_jobs(url: str, jobsite=jobnames.MCDEAN, company_id=None, state=None, max_jobs=10):
    async with async_playwright() as p:
        
        
        csv_filename = init_jobs_csv(jobsite)
        
        salary_pattern = re.compile(
            r"\$[\d,]+(?:\.\d+)?\s*(?:-|to)?\s*\$?[\d,]*(?:\.\d+)?(?:\s*(?:per\s*(?:hour|year)|/hour|/year))?",
            re.IGNORECASE
        )

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state("networkidle")  # Angular 

        results = []

        while True:

            await page.wait_for_selector(
                    'mat-expansion-panel.search-result-item a.job-title-link, a.read-more-button',
                    timeout=10000
                )

            jobs = page.locator("mat-expansion-panel.search-result-item")

            print(jobs)
            count = await jobs.count()
            print(f"Found {count} jobs on this page.")


            for i in range(count):
                
                try:
                    job_card = jobs.nth(i)
                    href = await job_card.locator("a.job-title-link").get_attribute("href")

                    if not href:
                        continue

                    job_url = urljoin(page.url, href)
                    
                    detail_page = await browser.new_page()
                    await detail_page.goto(job_url)
                    await detail_page.wait_for_selector("body")

                    detail_html = await detail_page.content()
                    
                    match = salary_pattern.search(detail_html)
                    salary = match.group(0) if match else "NA"

                
                    result = extract_description(detail_html)
                    results.append(result)

                    parsed_result = safe_parse_json(result)
                    job_data = normalize_job_data(parsed_result)
                    
                    if job_data is None:
                        print("Could not process job data correctly, skipping.")
                        continue

                    if os.path.exists(csv_filename):
                        try:
                            df = pd.read_csv(csv_filename)
                            existing_ids = set(df["job_id"].dropna().astype(str))
                        except FileNotFoundError:
                            existing_ids = set()

                    print("====================================================")
                    
                    if str(job_data["job_id"]) not in existing_ids:

                        job_data["salary"] = salary
                        job_data["job_url"] = str(job_url)
                        job_data["company"] = jobsite
                        job_data["company_id"] = company_id
                        job_data["last_scanned_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        
                        save_job_to_csv(csv_filename, job_data)
                        print(f"\nSaving job #{len(results) + 1}")
                            
                    else:
                        print(f"Job {job_data['job_id']} already exists. ")

                    await detail_page.close()

                    if len(results) >= max_jobs:
                        break
                except Exception as e:
                    print("Error:", e)
                    print(job_data)
                    continue
                
                finally:
                    print(detail_page)
                    if detail_page:
                        await detail_page.close()

            try:
                #load_more = await page.query_selector("text=/load more|more jobs|next/i")
                load_more = page.locator('button.mat-paginator-navigation-next')

                if await load_more.is_enabled():#load_more:
                    print("Clicking 'Load more'…")
                    await load_more.click()
                    #await page.wait_for_timeout(3000)
                    await page.wait_for_load_state('networkidle')
                    print("Clicked'Load more'…")
                    
                else:
                    print("No more pages.")
                    break
            except Exception as e:
                print("Error finding next page button:", e)
                break

        await browser.close()
        return results
    

async def scrape_capitalone_jobs(url: str,jobsite = jobnames.CAPITALONE, company_id=None, state=None,  max_jobs=10):
    async with async_playwright() as p:
        
        csv_filename = init_jobs_csv(jobsite)
        
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("body")

        current_page = int(await page.locator("input.pagination-current").input_value())
        total_pages_text = await page.locator("span.pagination-total-pages").inner_text()
        total_pages = int(total_pages_text.split()[-1])

        results = []

        while True:

            await page.wait_for_selector("#search-results-list li")
            jobs = page.locator("#search-results-list li")

            
            count = await jobs.count()
            limit = max_jobs if max_jobs is not None else count

            print(f"Found {count} jobs on this page.")
            print(jobs)
            print("=================")

            for i in range(min(max_jobs - len(results), count)): # just in case for max _jobs is defined
            #for i in range(min(limit - len(results), count)):
                print("Processing job =========== ")
                print(f"\nProcessing job after try #{len(results) + 1}")

                try:
                    print(f"\nProcessing job after try #{len(results) + 1}")
                    card = jobs.nth(i)
                    print(card)

                    href = await card.locator("a").get_attribute("href")
                    date = await card.locator(".job-date-posted").inner_text()

                    formatted_date = date
                    
                    if not href:
                        continue

                    job_url = urljoin(page.url, href)

                    detail_page = await browser.new_page()
                    await detail_page.goto(job_url)
                    await detail_page.wait_for_selector("body")

                    detail_html = await detail_page.content()

                    result = extract_description(detail_html)
                    results.append(result)

                    parsed_result = safe_parse_json(result)
                    
                    job_data = normalize_job_data(parsed_result)
                    
                    if job_data is None:
                        print("Could not process job data correctly, skipping.")
                        continue

                    if os.path.exists(csv_filename):
                        try:
                            df = pd.read_csv(csv_filename)
                            existing_ids = set(df["job_id"].dropna().astype(str))
                            existing_urls = set(df["job_url"].dropna().astype(str))
                            
                        except FileNotFoundError:
                            existing_ids = set()

                    if (str(job_url) not in existing_urls):
                        
                        job_data["posted_date"] = formatted_date
                        job_data["job_url"] = str(job_url)
                        job_data["company"] = jobsite
                        job_data["company_id"] = company_id
                        job_data["last_scanned_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        
                        save_job_to_csv(csv_filename, job_data)
                        print(f"\nSaving job #{len(results) + 1}")
                            
                    else:
                        print(f"Job {job_data['job_id']} already exists. ", "this is url ", job_url)

                    await detail_page.close()
    
                    if len(results) >= max_jobs:
                        break
                except Exception as e:
                    print("Error job reading:", e)
                    print(job_data)
                    
                    continue
                    
                finally:
                    if detail_page:
                        await detail_page.close()

            if len(results) >= max_jobs:
                break

            try:
                dialog = await page.query_selector("dialog#survale-survey-dialog[open]")
                if dialog:
                    close_button = await dialog.query_selector("button#survale-survey-dialog-close")
                    if close_button:
                        await close_button.click()
                        print("Dialog closed")
                        await page.wait_for_timeout(500)  
            except Exception as e:
                print("No dialog found or error closing it:", e)

            try:
                await page.evaluate("""
                    const dlg = document.querySelector('#survale-survey-dialog');
                    if (dlg) dlg.remove();
                """)
                await page.evaluate("""
                    const ifr = document.querySelector('#survale-survey-iframe');
                    if (ifr) ifr.remove();
                """)
                await page.evaluate("""
                    const banner = document.querySelector('#system-ialert');
                    if (banner) banner.remove();
                """)
                print("Popups removed")
            except Exception as e:
                print("No popups found:", e)


            try:
                banner_close = await page.query_selector("button#close_button")
                if banner_close:
                    await banner_close.click()
                    await page.wait_for_timeout(500)
                print('next page...')
                next_btn = page.locator("nav#pagination-bottom .next")
                if await next_btn.is_visible():
                    await next_btn.click()
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(2000)  

                else:
                    print("No more pages.")
                    break


                
            except Exception as e:
                print("Error finding next page button:", e)
                break


        await browser.close()
        return results
    

async def scrape_northrop_grumman_jobs(url: str, jobsite = jobnames.NG, company_id=None, state=None, max_jobs=10):

    async with async_playwright() as p:
        
        print('init ---- scrape_northrop_grumman_jobs method --- ')

        csv_filename = init_jobs_csv(jobsite)

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("body")


        while True:
            try:
                load_more = await page.query_selector("text='Show More Positions'")
                if load_more:
                    print("Clicking 'Load more'…")
                    await load_more.click()
                    await page.wait_for_timeout(2000)
                else:
                    break
            except:
                break


        results = []

        while True:

            await page.wait_for_selector("div.position-card")
            jobs = page.locator("div.position-card")
            count = await jobs.count()
            print(f"Found {count} jobs on this page.")
            
            
            for i in range(min(max_jobs - len(results), count)): # just in case for max _jobs is defined
                print("Processing job =========== ")
                print(f"\nProcessing job after try #{len(results) + 1}")
                
                try:
                    
                    card = jobs.nth(i)

                    await card.click()
                    await page.wait_for_timeout(1500)  
                    await page.wait_for_selector("div.position-container div.position-full-card")
                    container = await page.query_selector("div.position-container")
                    await page.wait_for_selector("div.position-job-description")

                    job_id_el = await container.query_selector("p.position-id-text")
                    job_id = await job_id_el.inner_text() if job_id_el else None
                    print("Job ID:", job_id)                

                    job_url = page.url
                    print("Job URL:", job_url)

                    container_html = await container.inner_html() # if container else None
                    result = extract_description(container_html)
                    results.append(result)

                    parsed_result = safe_parse_json(result)
                    job_data = normalize_job_data(parsed_result)
                    
                    if job_data is None:
                        print("Could not process job data correctly, skipping.")
                        continue

                    if os.path.exists(csv_filename):
                        try:
                            df = pd.read_csv(csv_filename)
                            existing_ids = set(df["job_id"].dropna().astype(str))
                        except FileNotFoundError:
                            existing_ids = set()

                    if str(job_data["job_id"]) not in existing_ids:
                        
                        job_data["job_url"] = str(job_url)
                        job_data["company"] = jobsite
                        job_data["last_scanned_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        
                        save_job_to_csv(csv_filename, job_data)
                        print(f"\nSaving job #{len(results) + 1}")
                            
                    else:
                        print(f"Job {job_data['job_id']} already exists. ")
    
                except Exception as e:
                    print("Error:", e)
                    print(job_data)
                    continue

            await browser.close()
            return results


async def scrape_jobs_load_more(url: str, jobsite = None, company_id=None, state=None, max_jobs=10):
    async with async_playwright() as p:
        
        csv_filename = init_jobs_csv(jobsite)

        date_formats = ["%m/%d/%Y", "%b %d, %Y", "%d-%b-%Y"]

        salary_pattern = re.compile(
            r"\$[\d,]+(?:\.\d+)?\s*(?:-|to)?\s*\$?[\d,]*(?:\.\d+)?(?:\s*(?:per\s*(?:hour|year)|/hour|/year))?",
            re.IGNORECASE
        )

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("body")


        while True:
            try:
                print("Clicking 'Show More Results'…")
                load_more = await page.query_selector("button:has-text('Show More Results')")
                #load_more = await page.query_selector("button:has-text('Show More Results'), button:has-text('More'), button[aria-label='Load more jobs']")
                
                if not load_more:
                    print('read more here')
                    buttons = page.locator("button[aria-label='Load more jobs']")
                    count = await buttons.count()
                    load_more = None
                    for i in range(count):
                        if await buttons.nth(i).is_visible():
                            load_more = buttons.nth(i)
                            break

                if not load_more:
                    print('read more here other')
                    load_more = await page.query_selector("ul.js-pager__items.pager a[rel='next']:has-text('Load More')")

                if not load_more:
                    print('read more here new tile button')
                    load_more = await page.query_selector("button#tile-more-results:has-text('More Search Results')")

                if not load_more:
                    load_more = await page.query_selector("text='Show More Positions'")
               

                print('the load_more is ',load_more )
                if load_more:
                    print("load_more: clicking 'Show More Results'…")
                    await load_more.click()
                    await page.wait_for_timeout(2000)
                else:
                    print("No botton, then scroll... ")
                    previous_height = await page.evaluate("document.body.scrollHeight")
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(2000)

                    new_height = await page.evaluate("document.body.scrollHeight")
                    if new_height == previous_height:
                        print("No hay más resultados al hacer scroll.")
                        break
                    else:
                        continue 
                    
            except Exception as e:
                print("Error clicking 'Show More Results':", e)
                break

        

        results = []


        print('reading job list...')
        while True:

            await page.wait_for_selector(
                        "ul.jobs-list__list, "
                        "ul#jobs, "
                        "div.views-infinite-scroll-content-wrapper, "
                        "ul.jobs-grid__list, "
                        "ul#job-tile-list, "
                        "div.position-card"
                    )
                                
            jobs = page.locator(
                                "ul.jobs-list__list > li[data-qa='searchResultItem'], "
                                "ul#jobs > li, "
                                "div.views-infinite-scroll-content-wrapper > div.views-row, "
                                "ul.jobs-grid__list > li[data-qa='searchResultItem'], "
                                "ul#job-tile-list > li.job-tile, "
                                "div.position-card"
                            )

            count = await jobs.count()
            print(f"Found {count} jobs on this page.")
            
            
            for i in range(min(max_jobs - len(results), count)): 
                
                print(f"\nProcessing job after try #{len(results) + 1}")
                
                try:

                    card = jobs.nth(i)
                    
                    link_locator = card.locator("a.job-list-item__link")
                    
                    if await link_locator.count() > 0:
                        href = await link_locator.first.get_attribute("href")
                    else:
                        link_locator_new = card.locator("div.views-field-field-workday-link a")
                        if await link_locator_new.count() > 0:
                            href = await link_locator_new.first.get_attribute("href")
                        else:
                            link_locator_grid = card.locator("a.job-grid-item__link")
                            if await link_locator_grid.count() > 0:
                                href = await link_locator_grid.first.get_attribute("href")
                            else:
                                link_locator_new2 = card.locator("a.jobTitle-link")
                                if await link_locator_new2.count() > 0:
                                    href = await link_locator_new2.first.get_attribute("href")
                                else:
                                    href = await card.locator("a").first.get_attribute("href")
                    
                    if href.startswith("http"):
                        job_url = href
                    else:
                        job_url = urljoin(page.url, href)

                    print("Job url:", job_url)

                    if company_id==jobnames.NG:
                        job_id_text = await page.locator(".position-full-card .position-id-text").inner_text()
                        print("job_id_text is ", job_id_text)


                    detail_page = await browser.new_page()
                    await detail_page.goto(job_url)
                    await detail_page.wait_for_selector("body")
                    await page.wait_for_timeout(4000)
                    
                    detail_html = await detail_page.content()

                    result = extract_description(detail_html)
                    results.append(result)
                    parsed_result = safe_parse_json(result)
                    job_data = normalize_job_data(parsed_result)
                    
                    if job_data is None:
                        print("Could not process job data correctly, skipping.")
                        continue

                    if os.path.exists(csv_filename):
                        try:
                            df = pd.read_csv(csv_filename)
                            existing_ids = set(df["job_id"].dropna().astype(str))
                            existing_urls = set(df["job_url"].dropna().astype(str))
                        except FileNotFoundError:
                            existing_ids = set()

                    if not state == None and (not jobsite == jobnames.UNDERARMOUR):

                        link = card.locator("a").first
                        city_state_div = await link.locator("div").first.text_content()
                        city_state_div = city_state_div.strip() if city_state_div else ""
                        city, state_detected = (s.strip() for s in city_state_div.split(",")) if "," in city_state_div else ("", "")
                        print('city and state ', city, state)
                        job_data['city'] = city
                        job_data['state'] = str(state)

                    clean_date = job_data.get("posted_date") 

                    formatted_date = None

                    if clean_date:
                        for fmt in date_formats:
                            try:
                                date_obj = datetime.strptime(clean_date, fmt)
                                formatted_date = date_obj.strftime("%Y-%m-%d")
                                break 
                            except ValueError:
                                continue

                        if formatted_date is None:
                            formatted_date = parse_relative_date(clean_date)

                    if formatted_date:
                        print("Formatted date:", formatted_date)
                    else:
                        print("Could not parse date:", clean_date)

                    
                    #if (str(job_url) not in existing_urls): #str(job_data["job_id"]) not in existing_ids:
                    if job_url not in existing_urls:
                        print('enter for saving ')
                        if not formatted_date == None:
                            job_data["posted_date"] = formatted_date

                        job_data["job_url"] = str(job_url)
                        job_data["company"] = jobsite
                        job_data["company_id"] = company_id
                        job_data["last_scanned_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        
                        save_job_to_csv(csv_filename, job_data)
                        print(f"\nSaving job #{len(results) + 1}")
                            
                    else:
                        print(f"Job {job_data['job_id']} already exists. ")

                    
                except Exception as e:
                    print("Error for saving :", e)
                    print(job_data)
                    continue
                    
                finally:
                    if detail_page:
                        await detail_page.close()

            await browser.close()
            return results


async def scrape_jobs_list_pagination(url: str, jobsite = "", company_id="", max_jobs=10):

    async with async_playwright() as p:
        
        
        csv_filename = init_jobs_csv(jobsite)
        
        salary_pattern = re.compile(
            r"\$[\d,]+(?:\.\d+)?\s*(?:-|to)?\s*\$?[\d,]*(?:\.\d+)?(?:\s*(?:per\s*(?:hour|year)|/hour|/year))?",
            re.IGNORECASE
        )

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        
        await page.wait_for_selector("body")

        results = []

        while True:
            
            await page.wait_for_selector(
                                        ".job-tile, "
                                        ".article--result, "
                                        "mat-expansion-panel.search-result-item, "
                                        "li.jobs-list-item, "
                                        "li.css-1q2dra3, "
                                        "div.job-item.job-item-posting, "
                                        "ul[data-ph-at-id='jobs-list'] > li.jobs-list-item"
                                    )
                                                
            jobs = page.locator(
                                ".job-tile, "
                                ".article--result, "
                                "mat-expansion-panel.search-result-item, "
                                "li.jobs-list-item, "
                                "li.css-1q2dra3, "
                                "div.job-item.job-item-posting, "
                                "ul[data-ph-at-id='jobs-list'] > li.jobs-list-item"
                            )
                                        

            count = await jobs.count()
            
            print(f"Found {count} jobs on this page.")

            print('number of ', max_jobs,len(results), count, min(max_jobs - len(results), count))
            
            for i in range(min(max_jobs - len(results), count)): 
            #for i in range(count): 
                
                print(f"\nProcessing job after try #{len(results) + 1}")

                try:
                    print(f"\nProcessing job after try #{len(results) + 1}")
                    card = jobs.nth(i)
                    
                    link_el = card.locator(
                        ".job-link, "
                        "h3.article__header__text__title a.link, "
                        "a.job-title-link, "
                        "a[data-ph-at-id='job-link'], "
                        "a[data-automation-id='jobTitle'], "
                        "a.btn.primary_button_color, "
                        "a[data-ph-at-id='job-link']"  
                    )

                    href = await link_el.first.get_attribute("href")

                    if href.startswith("http"):
                        job_url = href
                    else:
                        job_url = urljoin(page.url, href)

                    print("Job URL:", job_url)


                    clean_date = ""
                    formatted_date = None


                    try:
                        date_el = card.locator(".posting-date, span.list-item-posted, .job-postdate, dl dt:has-text('posted on') + dd")
                        date = await date_el.first.inner_text()
                        print("Posted date:", date)
                        clean_date = date.replace("Posted", "").replace("posted", "").replace("Posted Date", "").replace("Date", "").strip()
                        print("Posted date clean:", clean_date)
                    except Exception:
                        pass


                    if clean_date:
                        try:
                            date_obj = datetime.strptime(clean_date, "%m/%d/%Y")
                            formatted_date = date_obj.strftime("%Y-%m-%d")
                            print("Formatted date:", formatted_date)
                        except ValueError:
                            try:
                                date_obj = datetime.strptime(clean_date, "%b %d, %Y")
                                formatted_date = date_obj.strftime("%Y-%m-%d")
                                print("Formatted date:", formatted_date)
                            except ValueError:
                                try:
                                    date_obj = datetime.strptime(clean_date, "%d-%b-%Y")
                                    formatted_date = date_obj.strftime("%Y-%m-%d")
                                    print("Formatted date:", formatted_date)
                                except ValueError:
                                    formatted_date = parse_relative_date(clean_date)
                                    if formatted_date is None:
                                        print("Could not parse date:", clean_date)
                                        
                                    print("Formatted date:", formatted_date)

                    if not job_url:
                        continue
                    
                    print('==== this is the job url', job_url)


                    detail_page = await browser.new_page()
                    await detail_page.goto(job_url)
                    await detail_page.wait_for_selector("body")
                    #await page.wait_for_load_state("networkidle")
                    await page.wait_for_timeout(1000)


                    
                    detail_html = ""
                    json_ld = await detail_page.locator('script[type="application/ld+json"]').all_text_contents()

                    if json_ld:
                        detail_html = "\n".join(json_ld)
                    else:
                        detail_html = await detail_page.content()

                    
                    result = extract_description(detail_html)
                    results.append(result)
                    parsed_result = safe_parse_json(result)
                    job_data = normalize_job_data(parsed_result)
                    
                    if job_data is None:
                        print("Could not process job data correctly, skipping.")
                        continue

                    job_id = None

                    try:
                        job_id_el = card.locator("span.list-item-jobId, ul[data-automation-id='subtitle'] li")
    
                        if await job_id_el.count() > 0:
                            job_id_text = await job_id_el.first.inner_text()
                            if "#" in job_id_text:
                                job_id = job_id_text.split("#")[-1].strip()
                            else:
                                job_id = job_id_text.strip()
                                
                            job_data["job_id"] = job_id
                            print("Job ID:", job_id)
                    except Exception:
                        pass  


                    if os.path.exists(csv_filename):
                        try:
                            df = pd.read_csv(csv_filename)
                            existing_ids = set(df["job_id"].dropna().astype(str))
                            existing_urls = set(df["job_url"].dropna().astype(str))
                            
                        except FileNotFoundError:
                            existing_ids = set()


                    jobexist = False
                    
                    if False:#not str(job_data["job_id"]) == 'NA':
                        if str(job_data["job_id"]) not in existing_ids:
                            print('before saving ========= job_id ', str(job_data["job_id"]))
                            jobexist = False
                    if str(job_url) not in existing_urls:
                        print('before saving ========= job_url ', str(job_url))
                        jobexist = False


                    if jobexist == False:
                        print('during saving ========= ')
                        if not formatted_date == None:
                            job_data["posted_date"] = formatted_date

                        if jobsite == "medstarhealth":
                            match = salary_pattern.search(detail_html)
                            salary = match.group(0) if match else "NA"
                            job_data["salary"] = salary

                        job_data["job_url"] = str(job_url)
                        job_data["company"] = jobsite
                        job_data["company_id"] = company_id
                        job_data["last_scanned_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        
                        save_job_to_csv(csv_filename, job_data)
                        print(f"\nSaving job #{len(results) + 1}")
                        
                    else:
                        print(f"Job {job_data['job_id']} already exists. ")

                    await detail_page.close()
    
                    if len(results) >= max_jobs:
                        break

                except Exception as e:
                    print("Error saving job_data ====== :", e)
                    print(job_data)
                    continue
                    
                finally:
                    if detail_page:
                        await detail_page.close()

            try:
                
                if not jobsite=="medstarhealth":
                    next_button = await page.query_selector(
                                'button[aria-label="Next page"], '
                                'button[aria-label="Next Page of Job Search Results"], '
                                'a.paginationNextLink, '
                                'a.next-btn, '
                                'button[aria-label="next"], '
                                'a.next_page'
                            )
                else:
                    next_button = await page.query_selector("text=/load more|more jobs|next/i")
                
                
                if next_button:
                    tag = await next_button.get_property("tagName")
                    if (await tag.json_value()).lower() == "a":
                        next_url = await next_button.get_attribute("href")
                        await page.goto(urljoin(page.url, next_url))
                    else:
                        await next_button.click()
                    await page.wait_for_timeout(3000)
                else:
                    print("No more pages.")
                    break

            except Exception as e:
                print("Error finding next page:", e)
                break


        await browser.close()
        return results
    

async def scrape_pwcs(page, max_jobs):
    
    #await page.wait_for_selector("table")

    await page.wait_for_selector("body")

    row_locator = page.locator("table tr")
    count = await row_locator.count()
    print(f"Hay {count} filas en la tabla")
    
    jobs = []
    for i in range(count):
        if len(jobs) >= max_jobs:
            break

        row = row_locator.nth(i)
        cells = row.locator("td")
        cell_count = await cells.count()

        if cell_count == 0:
            continue

        job_data = []
        for j in range(cell_count):
            text = await cells.nth(j).inner_text()
            job_data.append(text.strip())

        jobs.append(job_data)

    print(f"{len(jobs)} jobs extracted.")

    return ''
