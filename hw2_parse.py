import requests
from bs4 import BeautifulSoup as bs
import sqlite3 as sql
from constants import *
import json

try:
    search_result = requests.get(url2, headers=user_agent)
    if search_result.status_code == 200:
        soup = bs(search_result.content, 'lxml')
        result = soup.find('template').text
        links = json.loads(result)
        data = []
        for link in links['vacancySearchResult']['vacancies']:
            vacancy_page = requests.get(link['links']['desktop'], headers=user_agent)
            if vacancy_page.status_code == 200:
                content = bs(vacancy_page.content, 'lxml')
                description = ''
                vd = content.find('div', attrs={'data-qa': 'vacancy-description'})
                if vd is not None:
                    description = vd.get_text()
                key_skills_containers = content.find_all('span', attrs={'data-qa': 'bloko-tag__text'})
                key_skills =''
                for skill in key_skills_containers:
                    key_skills += skill.text + ', '
                key_skills = key_skills[:-2]
                data.append([link['company']['name'], link['name'], description, key_skills])
        try:
            connection = sql.connect(db)
            cursor = connection.cursor()
            print(f"База данных {db} подключена к SQLite")
            tab_create = '''
            CREATE TABLE IF NOT EXISTS vacancies2(
                id integer primary key,
                employer_name text,
                name text,
                description text,
                key_skills text
            );'''
            cursor.execute(tab_create)
            connection.commit()
            print(f"Таблица {tab_create}\n успешно добавлена в БД")
            insert_val = "INSERT INTO vacancies2(employer_name, name, description, key_skills) VALUES(?, ?, ?, ?);"
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
    print("Исключение: ", OSError.__class__, OSError.args)