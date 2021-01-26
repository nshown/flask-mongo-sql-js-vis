#This setup file creates a postgresql database 
import os
from pymongo import MongoClient

db_name = "favorite_color"
table_name = "color_votes"

if 'MONGO_URL' in os.environ:
    mongo_url = os.environ['MONGO_URL']
else:
    #if we're not running in heroku then try and get my local config password
    import config
    db_name = config.db_name
    table_name = config.table_name
    mongo_url = "mongodb://localhost:27017/"

#Creating a pymongo client
client = MongoClient(mongo_url)

#delete database if it exists
client.drop_database(db_name)


#Getting the database instance
db = client[db_name]
print("Database created........")

#Creating a collection
collection = db[table_name]
print("Collection created........")

#define data
sp_to_en_colors = [{"votes": 62, "color":"red"},
                    {"votes": 24, "color":"orange"},
                    {"votes": 29, "color":"yellow"},
                    {"votes": 18, "color":"green"},
                    {"votes": 44, "color":"blue"},
                    {"votes": 64, "color":"black"},
                    {"votes": 48, "color":"pink"}]

res = collection.insert_many(sp_to_en_colors)
print("Data inserted ......")
print(res.inserted_ids)
