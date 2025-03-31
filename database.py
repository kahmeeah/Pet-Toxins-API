import sqlite3
import json

def insert_data(toxins):
    # define connection and cursor 

    connection = sqlite3.connect('pet_toxins.db')

    cursor = connection.cursor()

    #create toxins table

    createcommand = """CREATE TABLE IF NOT EXISTS
    toxins(toxin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE, category TEXT, link TEXT, image_url TEXT,
    alternate_names TEXT, description TEXT, symptoms TEXT,
    animals TEXT
    )"""

    cursor.execute(createcommand)

    # insert each toxin from toxins into table
    for toxin in toxins:
        cursor.execute("""INSERT INTO toxins (name, category, link, image_url, alternate_names, description, symptoms, animals
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?))
                       """, (
                           toxin["name"],
                           toxin["category"],
                           toxin["link"],
                           toxin["image_url"],
                           toxin["alternate_names"],
                           toxin["description"],
                           toxin["symptoms"],
                           json.dumps(toxin["animals"])
                       ))
        
    connection.commit()
    connection.close()