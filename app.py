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

