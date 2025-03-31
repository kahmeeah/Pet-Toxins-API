import requests
import re
from bs4 import BeautifulSoup
import sqlite3
def scrape_toxins():
    URL = "https://www.petpoisonhelpline.com/poisons/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    toxins = []

    letter_blocks = soup.find_all('li', {'id': re.compile(r'^[A-Z0-9]-block$')})

    for letter_block in letter_blocks:
        toxin_list = letter_block.find('ul', class_='slide')
        toxin_containers = toxin_list.find_all('li')

        for toxin_container in toxin_containers:
            toxin_name_element = toxin_container.find('a', class_='link-poison')
            toxin_name = toxin_name_element.text.strip()
            category_element = toxin_container.find('span', {'data-type': True})
            category = category_element.text.strip()

            toxin_link = toxin_name_element['href']
            toxin_page = requests.get(toxin_link, headers=headers)
            
            if toxin_page.status_code == 200:
                
                toxin_soup = BeautifulSoup(toxin_page.text, "html.parser")

                # get image 
                image_div = toxin_soup.find(class_='desktop-thumb')
                image_style = image_div.get('style')
                image_url = image_style.split("url('")[1].split("')")[0]

                # alternate names
                alternate_names = toxin_soup.find(class_='altenate-text').text.strip() if toxin_soup.find(class_='altenate-text') else None # No, this is not a typo
                # alternate_names = alternate_name_element.text.strip()

                # description
                description_class = toxin_soup.find(class_='poison-description')
                description = description_class.find("p").text.strip() if description_class and description_class.find("p") else None

                # symptoms
                symptoms_list = description_class.find_all("li")
                symptoms = ', '.join(li.text for li in symptoms_list) if symptoms_list else "None specified. Monitor for general illness symptoms such as vomiting, lethargy, difficulty dreathing, and behavioral changes."

                # severity level

                # which animals


                # animal_soup = toxin_soup.find("ul", class_='tab-buttons')
                animal_soup = toxin_soup.find("div", class_="tab-sections")
                if animal_soup and animal_soup.find_all(): # if div and div not empty -> find_all: h3 class title, p class toxic-desc
                    keys = animal_soup.find_all("h3", class_="title") # animal type
                    values = animal_soup.find_all("p", class_="toxi-desc") # severity level

                    if keys and values:
                        animals = {key.text: ({"severity": value.text.strip()} if value.text else None) for key, value in zip(keys, values)}
                    elif keys and not values:
                        animals = { key.text: {"severity": None} for key in keys}
                    else:
                        animals = {}
                else:
                    animals = {}

                
            else:
                print("Error:",toxin_page.status_code)


            # print("Toxin Name:", toxin_name)
            # print("Category:", category)
            # print("Link:", toxin_link)
            # print("Image Url:", image_url)
            # print("Alternate Names:", alternate_names)
            # print("Description:", description)
            # print("Symptoms:", symptoms)
            # print("Animals:", animals)
            toxin = {
                "name": toxin_name,
                "category": category,
                "link": toxin_link,
                "image_url": image_url,
                "alternate_names": alternate_names,
                "description": description,
                "symptoms": symptoms,
                "animals": animals,
            }
            toxins.append(toxin)
    return toxins
            