from constants import *
import requests
from bs4 import BeautifulSoup as bs
import sqlite3 as sql
import time
import logging
import logging.config
from pathlib import Path

config = Path('logger.conf').absolute()
logging.config.fileConfig(fname=config, disable_existing_loggers=False)
logger = logging.getLogger('hwLogger')
try:
    search_result = requests.get(url)
    if search_result.status_code == 200:
        vacancy_list = search_result.json().get('items')
        data = []
        start = time.time()
        for item in vacancy_list:
            vacancy_page = requests.get(item['url'])
            if vacancy_page.status_code == 200:
                vacancy = vacancy_page.json()
                description = ''
                key_skills = ''
                if (vacancy['description'] != None):
                    description = bs(vacancy['description'], 'lxml').get_text()
                if (vacancy['key_skills'] != None):
                    for skill in vacancy['key_skills']:
                        key_skills += skill['name'] + ', '
                    key_skills = key_skills[:-2]
                data.append([vacancy['employer']['name'], vacancy['name'], description, key_skills])
        logger.info(f"Время выполнения, с: {time.time() - start}")
        try:
            connection = sql.connect(db)
            cursor = connection.cursor()
            logger.info(f"База данных {db} подключена к SQLite")
            cursor.execute(tab_vacancies)
            connection.commit()
            logger.info('Таблица vacancies успешно добавлена в БД')
            cursor.executemany(insert_vacancy, data)
            connection.commit()
            logger.info('Данные успешно добавлены в таблицу vacancies')
            cursor.close()
        except sql.Error as error:
            logger.error('Не удалось вставить данные в таблицу vacancies')
            logger.error("Исключение: ", error.__class__, error.args)
        finally:
            if (connection):
                connection.close()
                logger.info("Соединение с SQLite закрыто")
    else:
        logger.critical(f"Не удалось загрузить данные поиска: {search_result.status_code}")
except Exception:
    logger.critical(f"Исключение: {Exception.__class__}, {Exception.args}")