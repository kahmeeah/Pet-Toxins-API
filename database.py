import sqlite3

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

# import list of toxins from scrapper.py
# insert each into table