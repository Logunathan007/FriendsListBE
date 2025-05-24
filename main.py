from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# PostgreSQL connection config
conn = psycopg2.connect(
    dbname='friends_swbb',
    user='logu_n_j',
    password='Ed2PMh2SJ3NQ5lMNe7jGK9z6UJkx8gDL',
    host='dpg-d0orl2emcj7s73dgeang-a.oregon-postgres.render.com',
    port='5432'
)

cursor = conn.cursor()

# ADD
@app.route('/add', methods=['POST'])
def add_name():
    try:
        data = request.get_json()
        cursor.execute("INSERT INTO names (name) VALUES (%s)", (data['name'],))
        conn.commit()
        return jsonify({'message': 'User Added', 'Failed': False})
    except Exception as e:
        return jsonify({'message': 'Failed to insert', 'error': str(e), 'Failed': True}), 500

# READ all
@app.route('/get', methods=['GET'])
def get_names():
    cursor.execute("SELECT name FROM names")
    rows = cursor.fetchall()
    return jsonify([i[0] for i in rows])

@app.route('/delete/<string:name>', methods=['DELETE'])
def delete_name(name):
    cursor.execute("DELETE FROM names WHERE name = %s", (name,))
    conn.commit()
    return jsonify({'message': 'Name deleted', 'Failed': False})

if __name__ == '__main__':
    app.run(debug=True)