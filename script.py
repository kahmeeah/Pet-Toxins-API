from scrapper import scrape_toxins
from database import insert_data

toxins = scrape_toxins()
insert_data(toxins)