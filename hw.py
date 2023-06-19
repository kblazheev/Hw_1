import zipfile
import pandas as pd
import sqlite3 as sql
with zipfile.ZipFile('okved_2.json.zip', 'r') as zip:
    zip.extract('okved_2.json')
okved_df = pd.read_json('okved_2.json')
db = 'hw.db'
connection = sql.connect(db)
cursor = connection.cursor()
tab_okved = '''
CREATE TABLE IF NOT EXISTS okved(
    id int primary key,
    code text,
    parent_code text,
    section text,
    name text,
    comment text
);'''
cursor.execute(tab_okved)
connection.commit()
insert_val = "INSERT INTO okved(code, parent_code, section, name, comment) VALUES(?, ?, ?, ?, ?);"
data = []
for index, row in okved_df.iterrows():
    data.append(row)
cursor.executemany(insert_val, data)
connection.commit()
cursor.close()
connection.close()