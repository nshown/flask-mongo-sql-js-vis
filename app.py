from flask import Flask, jsonify, render_template, redirect
import os
import sqlite3
import psycopg2
from pymongo import MongoClient
import socket


table_name = "color_votes"
db_name = "favorite_color"

#check if we're running in heroku and my environmental variable exist
if 'DATABASE_URL' in os.environ:
    postgres_url = os.environ['DATABASE_URL']
    mongo_url = os.environ['MONGO_URL']
else:
    #if we're not running in heroku then try and get my local config password
    from db import config
    postgres_url = f"postgresql://postgres:{config.postgres_pwd}@127.0.0.1:5432/{db_name}"
    mongo_url = "mongodb://localhost:27017/"


# Create an instance of Flask
app = Flask(__name__)

# Route to render most basic index.html template
@app.route("/")
def home():
    print("responding to home route request")
    # Return template and data
    return render_template("index.html")

# Route to render visualization by querying web api from JavaScript
@app.route("/chart")
def js_using_web_api():
    print("responding to /chart route request")
    return render_template("chart.html")

# Route that will return Web API JSON data from SQLite
@app.route("/sqlite-web-api")
def sqlite_web_api():
    conn = sqlite3.connect(f'db/{db_name}.db')

    cursor = conn.cursor()

    cursor.execute(f'''SELECT VOTES, COLOR from {table_name}''')

    results = cursor.fetchall()
    color_data_from_db = [ {"votes": result[0], "color": result[1]} for result in results]

    conn.close()
    
    print("responding to /sqlite-web-api route request")

    return jsonify(color_data_from_db)

# Route that will return Web API JSON data from PostgreSQL
@app.route("/postgresql-web-api")
def postgresql_web_api():
    # conn = psycopg2.connect(
    #     database=db_name, user='postgres', password=postgres_pwd, host='127.0.0.1', port= '5432'
    # )
    conn = psycopg2.connect(postgres_url)
    cursor = conn.cursor()

    cursor.execute(f'''SELECT VOTES, COLOR from {table_name}''')

    results = cursor.fetchall()
    color_data_from_db = [ {"votes": result[0], "color": result[1]} for result in results]

    conn.close()

    print("responding to /postgresql-web-api route request")
    return jsonify(color_data_from_db)

# Route that will return Web API JSON data from MongoDB
@app.route("/mongodb-web-api")
def mongodb_web_api():
    #client = MongoClient('localhost', 27017)
    client = MongoClient(mongo_url)

    db = client[db_name]

    collection = db[table_name]

    results = collection.find()
    
    #results is a cursor object, when looping through it each result is a dictionary
    color_data_from_db = [ {"votes": result["votes"], "color": result["color"]} for result in results]

    print("responding to /mongodb-web-api route request")
    return jsonify(color_data_from_db)

if __name__ == "__main__":
    app.run(debug=True)
