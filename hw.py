import zipfile
import pandas as pd
import sqlite3 as sql
from constants import *

print(okved_archive)
with zipfile.ZipFile(okved_archive, 'r') as zip:
    zip.extract(okved_file)
okved_df = pd.read_json(okved_file)

try:
    connection = sql.connect(db_name)
    cursor = connection.cursor()
    print(f"База данных {db_name} подключена к SQLite")
    tab_okved = '''
    CREATE TABLE IF NOT EXISTS okved(
        id integer primary key,
        code text,
        parent_code text,
        section text,
        name text,
        comment text
    );'''
    cursor.execute(tab_okved)
    connection.commit()
    print(f"Таблица {tab_okved}\n успешно добавлена в БД")
    insert_val = "INSERT INTO okved(code, parent_code, section, name, comment) VALUES(?, ?, ?, ?, ?);"
    data = []
    for index, row in okved_df.iterrows():
        data.append(row)
    cursor.executemany(insert_val, data)
    connection.commit()
    print("Данные успешно добавлены в таблицу")
    cursor.close()
except sql.Error as error:
    print("Не удалось вставить данные в таблицу")
    print("Исключение: ", error.__class__, error.args)
finally:
    if (connection):
        connection.close()
        print("Соединение с SQLite закрыто")