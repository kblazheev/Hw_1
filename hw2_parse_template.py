from constants import *
import requests
from bs4 import BeautifulSoup as bs
import sqlite3 as sql
import json
import logging
import logging.config
from pathlib import Path

config = Path('logger.conf').absolute()
logging.config.fileConfig(fname=config, disable_existing_loggers=False)
logger = logging.getLogger('hwLogger')
try:
    search_result = requests.get(url2, headers=user_agent, params=url_params)
    if search_result.status_code == 200:
        soup = bs(search_result.content, 'lxml')
        data = []
        result = soup.find('template').text
        links = json.loads(result)
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
                company = ''
                if 'name' in link['company'].keys():
                    company = link['company']['name']
                data.append([company, link['name'], description, key_skills])
        try:
            connection = sql.connect(db)
            cursor = connection.cursor()
            logger.info(f"База данных {db} подключена к SQLite")
            cursor.execute(tab_vacancies2)
            connection.commit()
            logger.info('Таблица vacancies2 успешно добавлена в БД')
            cursor.executemany(insert_vacancy2, data)
            connection.commit()
            logger.info('Данные успешно добавлены в таблицу')
            cursor.close()
        except sql.Error as error:
            logger.error('Не удалось вставить данные в таблицу vacancies2')
            logger.error(f"Исключение: {error.__class__}, {error.args}")
        finally:
            if (connection):
                connection.close()
                logger.info("Соединение с SQLite закрыто")
    else:
        logger.critical(f"Не удалось загрузить данные поиска: {search_result.status_code}")
except Exception:
    logger.critical(f"Исключение: {Exception.__class__}, {Exception.args}")