import sqlite3
from pymongo import MongoClient

def setup_mysql_db():
    conn = sqlite3.connect('travel_planner.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trips (
        trip_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        destination TEXT,
        start_date TEXT,
        end_date TEXT,
        budget REAL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')

    conn.commit()
    return conn

def setup_mongo_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['travel_planner']
    places_collection = db['places']
    return client, places_collection

if __name__ == "__main__":
    setup_mysql_db()
    setup_mongo_db()

