from playwright.sync_api import sync_playwright
import json

def get_page_html_only(url: str) -> str:
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

def get_page_html(url: str) -> str:
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
                    page.mouse.wheel(0, 2000)
                else:
                    break
            except Exception as e:
                print(f"Error - click : {e}")
                break

        text = page.inner_text("body")

        with open("debug_output.txt", "w") as f:
            f.write(text)
    
    
        job_cards = page.locator("div.job-list-item.card")
        count = job_cards.count()

        print(f"Found {count} jobs. Navegating to extraxt details...")
        
        jobs = []
        
        for i in range(count):
            job = job_cards.nth(i)
            job.click()
            page.wait_for_timeout(2000)  
            

        with open("debug_full_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        #browser.close()
        return text


def get_page(url: str):
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
    
        print('after get page')
        html = page.content()  
        
        with open("debug_output.txt", "w") as f:
            f.write(text)

        with open("debug_full_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        return page, html