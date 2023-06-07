import zipfile
import pandas as pd
import sqlite3 as sql
with zipfile.ZipFile('okved_2.json.zip', 'r') as zip:
    zip.extract('okved_2.json')
okved_df = pd.read_json('okved_2.json')
db = 'hw.db'
con = sql.connect(db)
q1 = '''
CREATE TABLE okved(
    code text,
    parent_code text,
    section text,
    name text,
    comment text
);'''
con.execute(q1)
for index, row in okved_df.iterrows():
    q2 = "INSERT INTO okved(code, parent_code, section, name, comment) VALUES(?, ?, ?, ?, ?);"
    con.execute(q2, row)
con.commit()
con.close()