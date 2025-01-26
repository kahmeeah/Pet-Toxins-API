import requests
import re
from bs4 import BeautifulSoup
import sqlite3

URL = "https://www.petpoisonhelpline.com/poisons/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")



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
            alternate_names = toxin_soup.find(class_='altenate-text').text.strip() # No, this is not a typo
            # alternate_names = alternate_name_element.text.strip()

            # description
            description_class = toxin_soup.find(class_='poison-description')
            description = description_class.find("p").text.strip()

            # symptoms
            symptoms_list = description_class.find_all("li")
            symptoms = ', '.join(li.text for li in symptoms_list)

            # severity level

            # which animals

            # animal_soup = toxin_soup.find("ul", class_='tab-buttons')
            animal_soup = toxin_soup.find("div", class_="tab-sections")
            if animal_soup and animal_soup.find_all(): # if div and div not empty
                # find_all: h3 class title, p class toxic-desc
                keys = animal_soup.find_all("h3", class_="title")
                values = animal_soup.find_all("p", class_="toxi-desc")
                # keys = animal type
                # value = severity level
                print(keys, values)
                print(len(keys))

                if not values:
                    print("Values true")
                    for key, value in zip(keys, values):
                        print("Key:", key.text)
                        print("Value:", value.text)
                        animals = {key.text: (value.text if value.text else None) for key, value in zip(keys, values)}
                    
                else:
                    print("Values false")
                    i = 0
                    values = []
                    while i < len(keys):
                        values.insert(i, None)
                        i += 1

                
            else:
                animals = None
            # else animals = None
            
        else:
            print("Error:",toxin_page.status_code)


        print("Toxin Name:", toxin_name)
        print("Category:", category)
        print("Link:", toxin_link)
        print("Image Url:", image_url)
        print("Alternate Names:", alternate_names)
        print("Description:", description)
        print("Symptoms:", symptoms)
        print("Animals:", animals)
        


# prints a list of every item on the list

# toxin_name = soup.find_all(class_="link-poison")

# toxin_category = soup.find_all('span' ,{'data-type': True})

# loop to create a single dict, append all to to list at end of loop

# for name in toxin_name:
#     print("Item: ", name.text)

# for category in toxin_category:
#      print("Category:", category.text)

# TO-DO: grab link from each item, go to link and grab additional info from there
#        also grab the category type