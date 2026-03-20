from ingestion.scraper import extract_information_from_page

link = "https://www.whatcar.com/audi/a7/hatchback/used-review/n20932/reliability"


content = extract_information_from_page(link)