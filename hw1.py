import zipfile
import pandas as pd
import sqlite3 as sql
import os
db = 'hw1.db'
#con = sql.connect(db)
q1 = '''
CREATE TABLE telecom_companies(
    name text,
    inn text,
    ogrn text,
    ogrn_date date,
    okved text
);'''
#con.execute(q1)
with zipfile.ZipFile('egrul.json.zip', 'r') as zip:
    files = zip.namelist()
    i = 1
    for file in files:
        if i == 5:
            break
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
                        print(row['name'], row['inn'], row['ogrn'], ogrn_date, okved)
                        continue
                if 'СвОКВЭДДоп' in row['data']['СвОКВЭД'].keys():
                    for item in row['data']['СвОКВЭД']['СвОКВЭДДоп']:
                        if not isinstance(item, str):
                            okved = item['КодОКВЭД']
                            if okved[:2] == '61':
                                print(row['name'], row['inn'], row['ogrn'], ogrn_date, okved)
                                break                    
        os.remove(file)
        i += 1       
#    q2 = "INSERT INTO okved(code, parent_code, section, name, comment) VALUES(?, ?, ?, ?, ?);"
#    con.execute(q2, row)
#con.commit()
#con.close()