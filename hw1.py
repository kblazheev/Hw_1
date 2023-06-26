import zipfile
import pandas as pd
import sqlite3 as sql
from constants import *

try:
    connection = sql.connect(db_telecom)
    cursor = connection.cursor()
    print(f"База данных {db_telecom} подключена к SQLite")
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
    print(f"Таблица {tab_create}\n успешно добавлена в БД")
except sql.Error as error:
    print(f"Не удалось добавить таблицу")
    print("Исключение: ", error.__class__, error.args)
    if (connection):
        connection.close()
        print("Соединение с SQLite закрыто")

data = []
insert_val = "INSERT INTO telecom_companies(name, inn, ogrn, ogrn_date, okved) VALUES(?, ?, ?, ?, ?);"

with zipfile.ZipFile(egrul_archive, 'r') as zip:
    names = zip.namelist()
    i = 1
    for name in names:
        if i > 50:
            break
        with zip.open(name) as file:
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
        i += 1    
try:
    cursor.executemany(insert_val, data)
    connection.commit()
    print(f"Данные успешно добавлены в таблицу")
    cursor.close()
except sql.Error as error:
    print(f"Не удалось вставить данные в таблицу")
    print("Исключение: ", error.__class__, error.args)
finally:
    if (connection):
        connection.close()
        print("Соединение с SQLite закрыто")