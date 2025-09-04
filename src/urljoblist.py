JOBS = [
    {"company_id": "001", 
     "company": "amazon", 
     "scrape_method":"scrape_jobs_list_pagination", 
     "urls": {
         "default": "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&country%5B%5D=USA&state%5B%5D=Virginia&state%5B%5D=Maryland&state%5B%5D=District%20of%20Columbia&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&"
        }
     },
    {"company_id": "002", 
     "company": "aecom", 
     "scrape_method":"scrape_jobs_load_more", 
     "urls": {
         "Virginia": "https://aecom.jobs/locations/virginia/jobs/",
         "Maryland": "https://aecom.jobs/locations/maryland/jobs/",
         "DC": "https://aecom.jobs/locations/district-of-columbia/jobs/"
        }
     },
    {"company_id": "003", 
     "company": "jobs_capitalone", 
     "scrape_method":"scrape_capitalone_jobs",
     "urls": {
         "Virginia": "https://www.capitalonecareers.com/search-jobs/Virginia%2C%20US/234/3/6252001-6254928/37x54812/-77x44675/50/2",
         "Maryland": "https://www.capitalonecareers.com/search-jobs/Maryland%20City%2C%20MD/234/4/6252001-4361885-4347283-4361831/39x09205/-76x81775/50/2",
         "DC": "https://www.capitalonecareers.com/search-jobs/District%20of%20Columbia%2C%20US/234/3/6252001-4138106/38x91706/-77x00025/50/2"
        }
     }, 
    {"company_id": "004", 
     "company": "clarkconstruction",
     "scrape_method":"scrape_jobs_load_more", 
     "urls": {
         "default": "https://www.clarkconstruction.com/build-your-career/search-apply?page=1"
        }
    },
    {"company_id": "005", 
     "company": "exelon", 
     "scrape_method": "scrape_jobs_list_pagination", 
     "urls": {
         "default": "https://jobs.exeloncorp.com/careers-home/jobs?state=Maryland%7CWashington,%20DC&page=1"
        }
    },
    {"company_id": "006", 
     "company": "george_washington_university", 
     "scrape_method":"scrape_jobs_list_pagination", 
     "urls": {
       "default": "https://www.gwu.jobs/postings/search"
        }
     },
    {"company_id": "007", 
     "company": "georgetown_university", 
     "scrape_method":"scrape_jobs_list_pagination", 
     "urls": {
         "default": "https://georgetown.wd1.myworkdayjobs.com/Georgetown_Admin_Careers"
        }
     },
    {"company_id": "008", 
     "company": "howard_university", 
     "scrape_method":"scrape_jobs_list_pagination", 
     "urls": {
         "default": "https://howard.wd1.myworkdayjobs.com/HU"
        }
    },
    {"company_id": "009", 
     "company": "inova", 
     "scrape_method":"scrape_jobs_load_more", 
     "urls": {
         "default" : "https://elar.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/jobs?mode=location"
        }
     },
    {"company_id": "010", 
     "company": "jhons_hopkins", 
     "scrape_method":"scrape_jobs_load_more", 
     "urls": {
         "default": "https://jobs.jhu.edu/search/?createNewAlert=false&q=&optionsFacetsDD_facility=&optionsFacetsDD_dept=&optionsFacetsDD_shifttype=&optionsFacetsDD_customfield1=&optionsFacetsDD_state="
        }
     },
    {"company_id": "011", 
     "company": "jp_morgan_chase", 
     "scrape_method":"scrape_jobs_list_pagination", 
     "urls": {
         "DC": "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/jobs?location=Washington%2C+DC%2C+United+States&locationId=300000020705795&locationLevel=city&mode=location&radius=25&radiusUnit=MI",
         "Maryland": "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/jobs?location=Maryland+City%2C+MD%2C+United+States&locationId=100000005729070&locationLevel=city&mode=location&radius=25&radiusUnit=MI"
        }
     }, 
    {"company_id": "012", 
     "company": "maximus", 
     "scrape_method":"scrape_jobs_list_pagination", 
     "urls": {
         "default": "https://maximus.avature.net/careers/SearchJobs/?6100=6047&6100_format=6846&6097=%5B11232%2C11245%2C11275%5D&6097_format=6843&listFilterMode=1&folderRecordsPerPage=6&"
        }
     },
    {"company_id": "013", 
     "company": "mcdean", 
     "scrape_method":"scrape_mcdean_jobs", 
     "urls": {
         "default": "https://careers.mcdean.com/jobs?page=1&locations=Aldie%C2%A0,Virginia,United%20States%7CAlexandria%C2%A0,Virginia,United%20States%7CAnnapolis%20Junction%C2%A0,Maryland,United%20States%7CAnnapolis,Maryland,United%20States%7CArlington%C2%A0,Virginia,United%20States%7CAshburn%C2%A0,Virginia,United%20States%7CBaltimore%C2%A0,Maryland,United%20States%7CBethesda%C2%A0,Maryland,United%20States%7CBoydton%C2%A0,Virginia,United%20States%7CCaroline%20County%C2%A0,Virginia,United%20States%7CChantilly%C2%A0,Virginia,United%20States%7CCharlottesville%C2%A0,Virginia,United%20States%7CChesapeake%C2%A0,Virginia,United%20States%7CChristiansburg%C2%A0,Virginia,United%20States%7CCollege%20Park%C2%A0,Maryland,United%20States%7CDistrict%20of%20Columbia,Washington~%20DC,United%20States%7CDulles%C2%A0,Virginia,United%20States%7CFairfax%C2%A0,Virginia,United%20States%7CFalls%20Church%C2%A0,Virginia,United%20States%7CFort%20Meade%C2%A0,Maryland,United%20States%7CFredericksburg%C2%A0,Virginia,United%20States%7CFrederick%C2%A0,Maryland,United%20States%7CFt.%20Belvoir,Virginia,United%20States%7CGaithersburg%C2%A0,Maryland,United%20States%7CHarrisonburg%C2%A0,Virginia,United%20States%7CLaurel%C2%A0,Maryland,United%20States%7CLeesburg%C2%A0,Virginia,United%20States%7CLottsburg%C2%A0,Virginia,United%20States%7CManassas%C2%A0,Virginia,United%20States%7CMcLean%C2%A0,Virginia,United%20States%7CNorfolk%C2%A0,Virginia,United%20States%7CRichmond%C2%A0,Virginia,United%20States%7CSouth%20Hill%C2%A0,Virginia,United%20States%7CSpringfield%C2%A0,Virginia,United%20States%7CSterling%C2%A0,Virginia,United%20States%7CTysons%C2%A0,Virginia,United%20States%7CUrbana%C2%A0,Maryland,United%20States%7CVirginia%20Beach%C2%A0,Virginia,United%20States%7CWarrenton%C2%A0,Virginia,United%20States%7CWashington%C2%A0,Washington~%20DC,United%20States%7CWinchester%C2%A0,Virginia,United%20States"
        }
    },
    {"company_id": "014", 
     "company": "medstarhealth", 
     "scrape_method":"scrape_jobs_list_pagination", 
     "urls": {
         "default": "https://careers.medstarhealth.org/global/en/search-results"
        }
     },
    {"company_id": "015", 
     "company": "northrop_grumman", 
     "scrape_method":"scrape_northrop_grumman_jobs", 
     "urls":{
         "Maryland": "https://jobs.northropgrumman.com/careers?pid=1340058149304&State=Maryland&triggerGoButton=false&triggerGoButton=true&source=APPLICANT_SOURCE-3-504",
         "Virginia": "https://jobs.northropgrumman.com/careers?pid=1340067610613&State=Virginia&triggerGoButton=false&triggerGoButton=true&source=APPLICANT_SOURCE-3-504"
        }
     },
    {"company_id": "016", 
     "company": "truist", 
     "scrape_method": "scrape_jobs_list_pagination", 
     "urls": {
         "default": "https://careers.truist.com/us/en/search-results?keywords="
        }
    },
    {"company_id": "017", 
     "company": "underarmour", 
     "scrape_method":"scrape_jobs_load_more", 
     "urls": {
         "Maryland": "https://careers.underarmour.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Maryland&geolocation=",
         "Virginia": "https://careers.underarmour.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=virginia&geolocation="
        }
     },
] 