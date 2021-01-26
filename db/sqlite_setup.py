#This setup file creates a sqlite database 
import sqlite3
import config
conn = sqlite3.connect(f'{config.db_name}.db')

cursor = conn.cursor()

sp_to_en_colors = [{"votes": 62, "color":"red"},
                    {"votes": 24, "color":"orange"},
                    {"votes": 29, "color":"yellow"},
                    {"votes": 18, "color":"green"},
                    {"votes": 44, "color":"blue"},
                    {"votes": 64, "color":"black"},
                    {"votes": 48, "color":"pink"}]

cursor.execute(f"DROP TABLE IF EXISTS {config.table_name}")

sql_query = f'''CREATE TABLE {config.table_name}(
   ID INTEGER PRIMARY KEY AUTOINCREMENT,
   VOTES        INTEGER,
   COLOR        CHAR(50)
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