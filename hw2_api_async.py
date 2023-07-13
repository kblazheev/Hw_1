from constants import *
import requests
from bs4 import BeautifulSoup as bs
import sqlite3 as sql
import asyncio
import time
from aiohttp import ClientSession as cs
from aiohttp import TCPConnector as tcpcn
import logging
import logging.config
from pathlib import Path

config = Path('logger.conf').absolute()
logging.config.fileConfig(fname=config, disable_existing_loggers=False)
logger = logging.getLogger('hwLogger')

async def get_vacancy(url, session):
    async with session.get(url=url) as vacancy_page:
        vacancy_json = await vacancy_page.json()
        return vacancy_json
        
async def main(items):
    connector = tcpcn(limit=10)
    async with cs(api_url, connector=connector) as session:
        tasks = []
        for item in items:
            url = f"/{item['url'][18:]}"
            tasks.append(asyncio.create_task(get_vacancy(url, session)))
        vacancies_json = await asyncio.gather(*tasks)
    for vacancy in vacancies_json:
        description = ''
        key_skills = ''
        if (vacancy['description'] != None):
            description = bs(vacancy['description'], 'lxml').get_text()
        if (vacancy['key_skills'] != None):
            for skill in vacancy['key_skills']:
                key_skills += skill['name'] + ', '
            key_skills = key_skills[:-2]
        data.append([vacancy['employer']['name'], vacancy['name'], description, key_skills])

try:
    search_result = requests.get(url, params=url_params)
    if search_result.status_code == 200:
        vacancy_list = search_result.json().get('items')
        data = []
        start = time.time()
        asyncio.run(main(vacancy_list))
        logger.info(f"Время выполнения, с: {time.time() - start}")
        try:
            connection = sql.connect(db)
            cursor = connection.cursor()
            logger.info(f"База данных {db} подключена к SQLite")
            cursor.execute(tab_vacancies1)
            connection.commit()
            logger.info('Таблица vacancies1 успешно добавлена в БД')
            cursor.executemany(insert_vacancy1, data)
            connection.commit()
            logger.info('Данные успешно добавлены в таблицу')
            cursor.close()
        except sql.Error as error:
            logger.error('Не удалось вставить данные в таблицу vacancies1')
            logger.error("Исключение: ", error.__class__, error.args)
        finally:
            if (connection):
                connection.close()
                logger.info("Соединение с SQLite закрыто")
    else:
        logger.critical(f"Не удалось загрузить данные поиска: {search_result.status_code}")
except Exception:
    logger.critical(f"Исключение: {Exception.__class__}, {Exception.args}")