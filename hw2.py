import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
from constants import *

try:
    search_result = requests.get(url)
    if search_result.status_code == 200:
        vacancy_list = search_result.json().get('items')
        data = []
        for item in vacancy_list:
            vacancy_page = requests.get(item['url'])
            if vacancy_page.status_code == 200:
                vacancy = vacancy_page.json()
                description = ''
                key_skills = ''
                if (vacancy['description'] != None):
                    description = BeautifulSoup(vacancy['description'], 'lxml').get_text()
                if (vacancy['key_skills'] != None):
                    for skill in vacancy['key_skills']:
                        key_skills += skill['name'] + ', '
                    key_skills = key_skills[:-2]
                data.append([vacancy['employer']['name'], vacancy['name'], description, key_skills])
        try:
            connection = sql.connect(db)
            cursor = connection.cursor()
            print(f"База данных {db} подключена к SQLite")
            tab_create = '''
            CREATE TABLE IF NOT EXISTS vacancies(
                id integer primary key,
                employer_name text,
                name text,
                description text,
                key_skills text
            );'''
            cursor.execute(tab_create)
            connection.commit()
            print(f"Таблица {tab_create}\n успешно добавлена в БД")
            insert_val = "INSERT INTO vacancies(employer_name, name, description, key_skills) VALUES(?, ?, ?, ?);"
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
    else:
        print(f'Не удалось загрузить данные поиска: {search_result.status_code}')
except:
    print('Отсутствует сетевое подключение')