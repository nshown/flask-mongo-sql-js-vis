#This setup file creates a postgresql database 
import config
#print(config.test_msg)

import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user='postgres', password=config.postgres_pwd, host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute(f"DROP DATABASE IF EXISTS {config.db_name}")

#Creating a database
cursor.execute(f"CREATE DATABASE {config.db_name}")
print("Database created successfully........")

#close the connection to reestablish database connect to the newly create database
conn.close()

conn = psycopg2.connect(
   database=config.db_name, user='postgres', password=config.postgres_pwd, host='127.0.0.1', port= '5432'
)
cursor = conn.cursor()

#define data
sp_to_en_colors = [{"votes": 62, "color":"red"},
                    {"votes": 24, "color":"orange"},
                    {"votes": 29, "color":"yellow"},
                    {"votes": 18, "color":"green"},
                    {"votes": 44, "color":"blue"},
                    {"votes": 64, "color":"black"},
                    {"votes": 48, "color":"pink"}]

cursor.execute(f"DROP TABLE IF EXISTS {config.table_name}")

sql_query = f'''CREATE TABLE {config.table_name}(
   ID SERIAL PRIMARY KEY,
   VOTES        INT,
   COLOR        VARCHAR(50)
);
'''

cursor.execute(sql_query)
conn.commit()
print("Table created successfully........")


for sp_to_en_color in sp_to_en_colors:
    cursor.execute(f'''INSERT INTO {config.table_name}(
    VOTES, COLOR) VALUES 
    ('{sp_to_en_color["votes"]}', '{sp_to_en_color["color"]}')''')

conn.commit()
print("Data added successfully........")

cursor.execute(f'''SELECT * from {config.table_name}''')

results = cursor.fetchall()
print(results)

conn.close()