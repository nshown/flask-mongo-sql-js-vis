#This setup file creates a postgresql database 
import config
from pymongo import MongoClient

#Creating a pymongo client
client = MongoClient('localhost', 27017)

#Getting the database instance
db = client[config.db_name]
print("Database created........")

#Creating a collection
collection = db[config.table_name]
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
