import zipfile
import pandas as pd
import sqlite3 as sql
import os
db = 'hw1.db'
connection = sql.connect(db)
cursor = connection.cursor()
tab_create = '''
CREATE TABLE IF NOT EXISTS telecom_companies(
    id integer primary key,
    name text,
    inn text,
    ogrn text,
    ogrn_date date,
    okved text
);'''
cursor.execute(tab_create)
connection.commit()
data = []
with zipfile.ZipFile('egrul.json.zip', 'r') as zip:
    files = zip.namelist()
    for file in files:
        zip.extract(file)
        egrul = pd.read_json(file)
        for index, row in egrul.iterrows():
            ogrn_date = ''
            if 'ДатаОГРН' in row['data'].keys():
                ogrn_date = row['data']['ДатаОГРН']
            if 'СвОКВЭД' in row['data'].keys():
                if 'СвОКВЭДОсн' in row['data']['СвОКВЭД'].keys():
                    okved = row['data']['СвОКВЭД']['СвОКВЭДОсн']['КодОКВЭД']
                    if okved[:2] == '61':
                        data.append([row['name'], row['inn'], row['ogrn'], ogrn_date, okved])
        os.remove(file)   
insert_val = "INSERT INTO telecom_companies(name, inn, ogrn, ogrn_date, okved) VALUES(?, ?, ?, ?, ?);"
cursor.executemany(insert_val, data)
connection.commit()
cursor.close()
connection.close()