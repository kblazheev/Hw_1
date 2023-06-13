import zipfile
import pandas as pd
import sqlite3 as sql
#with zipfile.ZipFile('egrul.json.zip', 'r') as zip:
#    zip.extractall(path='.\egrul')
db = 'hw1.db'
#con = sql.connect(db)
q1 = '''
CREATE TABLE telecom_companies(
    name text,
    inn text,
    okved text,
    name text,
    comment text
);'''
#con.execute(q1)
i = 1
egrul = pd.read_json('00001.json')
for index, row in egrul.iterrows():
    if i == 1:
        i += 1
        continue
    codes = set()
    if 'CвОКВЭД' in row['data']:
        if 'CвОКВЭДДоп' in row['data']['СвОКВЭД']:
            for item in row['data']['СвОКВЭД']['CвОКВЭДДоп']:
                if len(item['КодОКВЭД']):
                    codes.append(item['КодОКВЭД'][:2])
        if 'CвОКВЭДОсн' in row['data']['СвОКВЭД']:
            if len(item['КодОКВЭД']):
                codes.append(row['data']['СвОКВЭД']['CвОКВЭДОсн']['КодОКВЭД'][:2])
    break
    #q2 = "INSERT INTO okved(code, parent_code, section, name, comment) VALUES(?, ?, ?, ?, ?);"
    #con.execute(q2, row)
#con.commit()
#con.close()