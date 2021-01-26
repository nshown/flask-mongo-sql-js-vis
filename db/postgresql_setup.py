#This setup file creates a postgresql database 
import psycopg2
import os

table_name = "color_votes"

if 'DATABASE_URL' in os.environ:
   postgres_url = os.environ['DATABASE_URL']
else:
   #if we're not running in heroku then try and get my local config password
   import config
   table_name = config.table_name
   postgres_url = f"postgresql://postgres:{config.postgres_pwd}@127.0.0.1:5432/{config.db_name}"

   #if local, try and delete and recreate the database to start afresh
   #establishing the connection
   conn = psycopg2.connect(f"postgresql://postgres:{config.postgres_pwd}@127.0.0.1:5432/postgres")

   #Creating a cursor object using the cursor() method
   cursor = conn.cursor()

   conn.autocommit = True

   cursor.execute(f"DROP DATABASE IF EXISTS {config.db_name}")

   #Creating a database
   cursor.execute(f"CREATE DATABASE {config.db_name}")
   print("Database created successfully........")

   #close the connection to reestablish database connect to the newly create database
   conn.close()

conn = psycopg2.connect(postgres_url)

conn.autocommit = True

cursor = conn.cursor()

#define data
sp_to_en_colors = [{"votes": 62, "color":"red"},
                    {"votes": 24, "color":"orange"},
                    {"votes": 29, "color":"yellow"},
                    {"votes": 18, "color":"green"},
                    {"votes": 44, "color":"blue"},
                    {"votes": 64, "color":"black"},
                    {"votes": 48, "color":"pink"}]

cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

sql_query = f'''CREATE TABLE {table_name}(
   ID SERIAL PRIMARY KEY,
   VOTES        INT,
   COLOR        VARCHAR(50)
);
'''

cursor.execute(sql_query)
conn.commit()
print("Table created successfully........")


for sp_to_en_color in sp_to_en_colors:
    cursor.execute(f'''INSERT INTO {table_name}(
    VOTES, COLOR) VALUES 
    ('{sp_to_en_color["votes"]}', '{sp_to_en_color["color"]}')''')

conn.commit()
print("Data added successfully........")

cursor.execute(f'''SELECT * from {table_name}''')

results = cursor.fetchall()
print(results)

conn.close()