
# to run this program click on run button or then click on link whick is display in terminal 
# "http://127.0.0.1:5000"
# or navigate to app.py directory and enter python app.py in terminal
from flask import Flask, request, jsonify, render_template, g
from pymongo import MongoClient
from db_setup import setup_mysql_db, setup_mongo_db
from foursquare_api import fetch_places_data

# Specify the path to the templates and static folders
template_folder_path = 'F:/Coding/PROJECTS/travel_planer/trip_planer/frontend/'
static_folder_path = 'F:/Coding/PROJECTS/travel_planer/static/'

# Initialize the Flask app with the specified template and static folder paths
app = Flask(__name__, template_folder=template_folder_path, static_folder=static_folder_path)

# Foursquare API credentials (consider using environment variables instead)
CLIENT_ID = 'YOUR_FOURSQUARE_CLIENT_ID'
CLIENT_SECRET = 'YOUR_FOURSQUARE_CLIENT_SECRET'

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')

# Access the database and collection
db = client['travel_database']
places_collection = db['travel_collection']

def get_db():
    if 'db' not in g:
        g.db = setup_mysql_db()
    return g.db

def get_cursor():
    if 'cursor' not in g:
        g.cursor = get_db().cursor()
    return g.cursor

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    cursor = g.pop('cursor', None)

    if cursor is not None:
        cursor.close()
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    try:
        cursor = get_cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (data['username'], data['email']))
        get_db().commit()
        return jsonify({"status": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/add_trip', methods=['POST'])
def add_trip():
    data = request.json
    try:
        cursor = get_cursor()
        cursor.execute("INSERT INTO trips (user_id, destination, start_date, end_date, budget) VALUES (?, ?, ?, ?, ?)", 
                       (data['user_id'], data['destination'], data['start_date'], data['end_date'], data['budget']))
        get_db().commit()
        # Fetch places data for the destination and save to MongoDB
        places_data = fetch_places_data(data['destination'], CLIENT_ID, CLIENT_SECRET)
        if places_data:
            places_collection.insert_many(places_data)
        return jsonify({"status": "Trip added successfully", "places": places_data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/users', methods=['GET'])
def get_users():
    try:
        cursor = get_cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        # Fetch column names from cursor description
        columns = [column[0] for column in cursor.description]
        # Map column names to each row and convert to dictionary
        users_with_columns = [{columns[i]: user[i] for i in range(len(columns))} for user in users]
        return jsonify(users_with_columns)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/trips', methods=['GET'])
def get_trips():
    try:
        cursor = get_cursor()
        cursor.execute("SELECT * FROM trips")
        trips = cursor.fetchall()
        # Fetch column names from cursor description
        columns = [column[0] for column in cursor.description]
        # Map column names to each row and convert to dictionary
        trips_with_columns = [{columns[i]: trip[i] for i in range(len(columns))} for trip in trips]
        return jsonify(trips_with_columns)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/places', methods=['GET'])
def get_places():
    try:
        places = list(places_collection.find())
        for place in places:
            place['_id'] = str(place['_id'])
        return jsonify(places)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
