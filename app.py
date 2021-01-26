from flask import Flask, jsonify, render_template, redirect
import os
import sqlite3
import psycopg2
from pymongo import MongoClient

table_name = "color_votes"
db_name = "favorite_color"

#check if we're running in heroku and my environmental variable exist
if 'POSTGRESQL_PASSWORD' in os.environ:
    postgres_pwd = os.environ['POSTGRESQL_PASSWORD']
else:
    #if we're not running in heroku then try and get my local config password
    from db import config
    postgres_pwd = config.postgres_pwd

# Create an instance of Flask
app = Flask(__name__)

# Route to render most basic index.html template
@app.route("/")
def home():
    # Return template and data
    return render_template("index.html")

# Route to render visualization by querying web api from JavaScript
@app.route("/chart")
def js_using_web_api():
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

    return jsonify(color_data_from_db)

# Route that will return Web API JSON data from PostgreSQL
@app.route("/postgresql-web-api")
def postgresql_web_api():
    conn = psycopg2.connect(
        database=db_name, user='postgres', password=postgres_pwd, host='127.0.0.1', port= '5432'
    )
    cursor = conn.cursor()

    cursor.execute(f'''SELECT VOTES, COLOR from {table_name}''')

    results = cursor.fetchall()
    color_data_from_db = [ {"votes": result[0], "color": result[1]} for result in results]

    conn.close()

    return jsonify(color_data_from_db)

# Route that will return Web API JSON data from MongoDB
@app.route("/mongodb-web-api")
def scrape():
    client = MongoClient('localhost', 27017)

    db = client[db_name]

    collection = db[table_name]

    results = collection.find()
    
    #results is a cursor object, when looping through it each result is a dictionary
    color_data_from_db = [ {"votes": result["votes"], "color": result["color"]} for result in results]

    
    return jsonify(color_data_from_db)



if __name__ == "__main__":
    app.run(debug=True)
