from build.scraper import scrape_toxins
from build.database import insert_data

toxins = scrape_toxins()
insert_data(toxins)