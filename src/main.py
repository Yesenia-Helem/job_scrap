import asyncio
import json
from urljoblist import jobs

from scrap_wp import scrape_jobs_list_pagination, scrape_jobs_load_more, scrape_capitalone_jobs, scrape_mcdean_jobs, scrape_northrop_grumman_jobs

def get_company_job(obs, company_name, company_id):
    return next((job for job in obs if job["company"] == company_name), None)


if __name__ == "__main__":

    url = "https://www.amazon.jobs/en/search" 
    
    url = "https://careers.medstarhealth.org/global/en/search-results"
    
    url = "https://careers.medstarhealth.org/global/en/search-results?from=1400&s=1"

    #url = "https://careers.medstarhealth.org/global/en/search-results?from=1300&s=1"
    url = "https://careers.mcdean.com/jobs?page=1&locations=Aldie%C2%A0,Virginia,United%20States%7CAlexandria%C2%A0,Virginia,United%20States%7CAnnapolis%20Junction%C2%A0,Maryland,United%20States%7CAnnapolis,Maryland,United%20States%7CArlington%C2%A0,Virginia,United%20States%7CAshburn%C2%A0,Virginia,United%20States%7CBaltimore%C2%A0,Maryland,United%20States%7CBethesda%C2%A0,Maryland,United%20States%7CBoydton%C2%A0,Virginia,United%20States%7CCaroline%20County%C2%A0,Virginia,United%20States%7CChantilly%C2%A0,Virginia,United%20States%7CCharlottesville%C2%A0,Virginia,United%20States%7CChesapeake%C2%A0,Virginia,United%20States%7CChristiansburg%C2%A0,Virginia,United%20States%7CCollege%20Park%C2%A0,Maryland,United%20States%7CDistrict%20of%20Columbia,Washington~%20DC,United%20States%7CDulles%C2%A0,Virginia,United%20States%7CFairfax%C2%A0,Virginia,United%20States%7CFalls%20Church%C2%A0,Virginia,United%20States%7CFort%20Meade%C2%A0,Maryland,United%20States%7CFredericksburg%C2%A0,Virginia,United%20States%7CFrederick%C2%A0,Maryland,United%20States%7CFt.%20Belvoir,Virginia,United%20States%7CGaithersburg%C2%A0,Maryland,United%20States%7CHarrisonburg%C2%A0,Virginia,United%20States%7CLaurel%C2%A0,Maryland,United%20States%7CLeesburg%C2%A0,Virginia,United%20States%7CLottsburg%C2%A0,Virginia,United%20States%7CManassas%C2%A0,Virginia,United%20States%7CMcLean%C2%A0,Virginia,United%20States%7CNorfolk%C2%A0,Virginia,United%20States%7CRichmond%C2%A0,Virginia,United%20States%7CSouth%20Hill%C2%A0,Virginia,United%20States%7CSpringfield%C2%A0,Virginia,United%20States%7CSterling%C2%A0,Virginia,United%20States%7CTysons%C2%A0,Virginia,United%20States%7CUrbana%C2%A0,Maryland,United%20States%7CVirginia%20Beach%C2%A0,Virginia,United%20States%7CWarrenton%C2%A0,Virginia,United%20States%7CWashington%C2%A0,Washington~%20DC,United%20States%7CWinchester%C2%A0,Virginia,United%20States"
    #url = "https://careers.mcdean.com/jobs?page=62&locations=Aldie%C2%A0,Virginia,United%20States%7CAlexandria%C2%A0,Virginia,United%20States%7CAnnapolis%20Junction%C2%A0,Maryland,United%20States%7CAnnapolis,Maryland,United%20States%7CArlington%C2%A0,Virginia,United%20States%7CAshburn%C2%A0,Virginia,United%20States%7CBaltimore%C2%A0,Maryland,United%20States%7CBethesda%C2%A0,Maryland,United%20States%7CBoydton%C2%A0,Virginia,United%20States%7CCaroline%20County%C2%A0,Virginia,United%20States%7CChantilly%C2%A0,Virginia,United%20States%7CCharlottesville%C2%A0,Virginia,United%20States%7CChesapeake%C2%A0,Virginia,United%20States%7CChristiansburg%C2%A0,Virginia,United%20States%7CCollege%20Park%C2%A0,Maryland,United%20States%7CDistrict%20of%20Columbia,Washington~%20DC,United%20States%7CDulles%C2%A0,Virginia,United%20States%7CFairfax%C2%A0,Virginia,United%20States%7CFalls%20Church%C2%A0,Virginia,United%20States%7CFort%20Meade%C2%A0,Maryland,United%20States%7CFredericksburg%C2%A0,Virginia,United%20States%7CFrederick%C2%A0,Maryland,United%20States%7CFt.%20Belvoir,Virginia,United%20States%7CGaithersburg%C2%A0,Maryland,United%20States%7CHarrisonburg%C2%A0,Virginia,United%20States%7CLaurel%C2%A0,Maryland,United%20States%7CLeesburg%C2%A0,Virginia,United%20States%7CLottsburg%C2%A0,Virginia,United%20States%7CManassas%C2%A0,Virginia,United%20States%7CMcLean%C2%A0,Virginia,United%20States%7CNorfolk%C2%A0,Virginia,United%20States%7CRichmond%C2%A0,Virginia,United%20States%7CSouth%20Hill%C2%A0,Virginia,United%20States%7CSpringfield%C2%A0,Virginia,United%20States%7CSterling%C2%A0,Virginia,United%20States%7CTysons%C2%A0,Virginia,United%20States%7CUrbana%C2%A0,Maryland,United%20States%7CVirginia%20Beach%C2%A0,Virginia,United%20States%7CWarrenton%C2%A0,Virginia,United%20States%7CWashington%C2%A0,Washington~%20DC,United%20States%7CWinchester%C2%A0,Virginia,United%20States"

    #url = "https://www.capitalonecareers.com/search-jobs"


    url = "https://jobs.northropgrumman.com/careers?pid=1340058149304&State=Maryland&triggerGoButton=false&triggerGoButton=true&source=APPLICANT_SOURCE-3-504"

    url = "https://elar.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/jobs?mode=location" #inova

    url = "https://jobs.jhu.edu/search/?createNewAlert=false&q=&optionsFacetsDD_facility=&optionsFacetsDD_dept=&optionsFacetsDD_shifttype=&optionsFacetsDD_customfield1=&optionsFacetsDD_state="
    
    url = "https://maximus.avature.net/careers/SearchJobs/?6100=6047&6100_format=6846&6097=%5B11232%2C11245%2C11275%5D&6097_format=6843&listFilterMode=1&folderRecordsPerPage=6&"

    url = "https://maximus.avature.net/careers/SearchJobs/?6100=6047&6100_format=6846&6097=%5B11232%2C11245%2C11275%5D&6097_format=6843&listFilterMode=1&folderRecordsPerPage=6&"

    url = "https://jobs.exeloncorp.com/careers-home/jobs?state=Maryland%7CWashington,%20DC&page=1"

    url = "https://careers.truist.com/us/en/search-results?keywords="

    url = "https://georgetown.wd1.myworkdayjobs.com/Georgetown_Admin_Careers"

    url = "https://aecom.jobs/locations/virginia/jobs/"
    url = "https://aecom.jobs/locations/maryland/jobs/"
    url = "https://aecom.jobs/locations/district-of-columbia/jobs/"
    
    url = "https://www.clarkconstruction.com/build-your-career/search-apply?page=1"

    url = "https://howard.wd1.myworkdayjobs.com/HU" #scrape_maximus_amazon_jobs

    url = "https://www.gwu.jobs/postings/search"

    url = "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/jobs?location=Washington%2C+DC%2C+United+States&locationId=300000020705795&locationLevel=city&mode=location&radius=25&radiusUnit=MI"


    url = "https://careers.underarmour.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Maryland&geolocation="

    url = "https://careers.underarmour.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=virginia&geolocation="
    
    #results = asyncio.run(scrape_amazon_jobs(url, max_jobs=3000))
    #results = asyncio.run(scrape_medstar_jobs(url, max_jobs=4000))
    #results = asyncio.run(scrape_mcdean_jobs(url, max_jobs=4000))
    #results = asyncio.run(scrape_dynamic_jobs(url, max_jobs=30))
    #results = asyncio.run(scrape_amazon_jobs(url, max_jobs=3000))
    #results = asyncio.run(scrape_capitalone_jobs(url, max_jobs=4000))
    #results = asyncio.run(scrape_northrop_grumman_jobs(url, max_jobs=3000))
    #results = asyncio.run(scrape_inova_jobs(url, max_jobs=3000))
    #results = asyncio.run(scrape_jhons_hopkins_jobs(url, max_jobs=3000))
    
    #results = asyncio.run(scrape_maximus_amazon_jobs(url, jobsite = "george_washington_niversity", max_jobs=4000))

    #results = asyncio.run(scrape_inova_aecom_jobs(url, jobsite = "underarmour", state=None, max_jobs=4000))

    

    job_selected = get_company_job(jobs, "northrop_grumman", "015")


    url = job_selected["url"]
    company = job_selected["company"]
    company_id = job_selected["company_id"]


    print(url, company, company_id)
    #for job in jobs:
    #    url = job["url"]
    #    company = job["company"]
    #    company_id = job["company_id"]

    #    print(f"Scraping {company} - {url}")
        
    sw = True

    if sw:
        results = asyncio.run(
                scrape_jobs_list_pagination(
                    url,
                    jobsite=company,
                    company_id=company_id,
                    state=None, 
                    max_jobs=4000
                )
            )

    else:
        results = asyncio.run(
            scrape_jobs_load_more(
                url, 
                jobsite = company, 
                company_id=company_id,
                state=None, 
                max_jobs=4000))

 #       print(json.dumps(results, indent=2))

#        break


# scrape_jobs_list_pagination : list and next button with pages-> amazon, 
# scrape_jobs_load_more: load more pages and collect each card
# :check state for which website is
#
