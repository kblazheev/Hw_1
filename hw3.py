from constants import *
import sqlite3 as sql
import logging
import logging.config
from pathlib import Path
from normalizer import normal
from collections import Counter

config = Path('logger.conf').absolute()
logging.config.fileConfig(fname=config, disable_existing_loggers=False)
logger = logging.getLogger('hwLogger')

try:
    connection = sql.connect(db)
    cursor = connection.cursor()
    logger.info(f"База данных {db} подключена к SQLite")
    # alter_vacancies = "ALTER TABLE vacancies1 ADD COLUMN normal_name text;"
    # alter_telecom_companies = "ALTER TABLE telecom_companies ADD COLUMN normal_name text;"
    # cursor.execute(alter_vacancies)
    # connection.commit()
    # logger.info('Таблица vacancies1 успешно изменена')
    # cursor.execute(alter_telecom_companies)
    # connection.commit()
    # logger.info('Таблица telecom_companies успешно изменена')
    # update_vacancies = "UPDATE vacancies1 SET normal_name = ? WHERE employer_name = ?"
    # select_vacancies = "SELECT employer_name FROM vacancies1;"
    # cursor.execute(select_vacancies)
    # for item in cursor.fetchall():
    #     cursor.execute(update_vacancies, [normal(item[0]), item[0]])
    # connection.commit()
    # update_vacancies = "UPDATE telecom_companies SET normal_name = ? WHERE name = ?"
    # select_vacancies = "SELECT name FROM telecom_companies;"
    # cursor.execute(select_vacancies)
    # for item in cursor.fetchall():
    #     cursor.execute(update_vacancies, [normal(item[0]), item[0]])
    # connection.commit()
    joiner = """
        SELECT vacancies1.employer_name, vacancies1.key_skills, telecom_companies.name, max(telecom_companies.okved)
        FROM vacancies1 INNER JOIN telecom_companies
        ON telecom_companies.normal_name LIKE vacancies1.normal_name
        GROUP BY vacancies1.employer_name;"""
    cursor.execute(joiner)
    skills = []
    for item in cursor.fetchall():
        # print(item)
        skills.extend(item[1].replace(' ', '').split(','))
    c = Counter(skills)
    for skill in c.most_common(10):
        print(f"{skill[1]}".rjust(2), ' - ', skill[0])
    logger.info("Запрос успешно выполнен")
    cursor.close()
except sql.Error as error:
    logger.critical("Не удалось выполнить запрос")
    logger.criticallogger.error(f"Исключение: {error.__class__}, {error.args}")
finally:                    
    if (connection):
        connection.close()
        logger.info("Соединение с SQLite закрыто")