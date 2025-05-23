from flask import Flask, jsonify, request
import sqlite3
import json

app = Flask(__name__)
app.json.sort_keys = False
DATABASE = "pet_toxins.db"

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row  #to get dictlike rows
    return connection

# default route
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Pet Toxins API"
    })

# get available routes and categories
@app.route("/endpoints", methods=["GET"])
def get_endpoints_and_filters():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT category FROM toxins")
    raw_categories = [row["category"] for row in cursor.fetchall()]
    normalized = {cat.strip().title() for cat in raw_categories if cat}
    categories = sorted(normalized)

    cursor.execute("SELECT animals FROM toxins")
    animal_keys = set()
    for row in cursor.fetchall():
        animals = json.loads(row["animals"])
        for key in animals.keys():
            animal_keys.add(key)

    connection.close()

    return jsonify({
        "routes": [
            { "method": "GET", "path": "/toxins", "description": "Get all toxins (filters: name, animal, category)" },
            { "method": "GET", "path": "/toxins/<id>", "description": "Get a specific toxin by ID" },
            { "method": "GET", "path": "/endpoints", "description": "List filterable categories, animals, and all routes" }
        ],
        "categories": sorted(categories),
        "animals": sorted(animal_keys)
    })


# get all toxins, get all toxins by param
@app.route("/toxins", methods=["GET"])
def get_toxins():
    name = request.args.get("name")
    animal = request.args.get("animal")
    category = request.args.get("category")

    query = "SELECT * FROM toxins WHERE 1=1"
    params = []

    if name:
        query += " AND LOWER(name) LIKE ?"
        params.append(f"%{name.lower()}%")
    if category:
        query += " AND LOWER(category) = ?"
        params.append(category.lower())
    if animal:
        animal = animal.title()
        query += " AND json_extract(animals, ?) IS NOT NULL"
        params.append(f"$.{animal}")

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()

    toxins = []
    for row in rows:
        toxin = dict(row)
        toxin["animals"] = json.loads(toxin["animals"])
        toxins.append(toxin)

    return jsonify(toxins)

# get toxin by id
@app.route("/toxins/<int:id>", methods=["GET"])
def get_toxin_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM toxins WHERE toxin_id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Toxin not found"}), 404

    toxin = dict(row)
    toxin["animals"] = json.loads(toxin["animals"])
    return jsonify(toxin)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  

