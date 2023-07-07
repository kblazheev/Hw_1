from constants import *
import zipfile
import pandas as pd
import sqlite3 as sql
import logging
import logging.config
from pathlib import Path

config = Path('logger.conf').absolute()
logging.config.fileConfig(fname=config, disable_existing_loggers=False)
logger = logging.getLogger('hwLogger')

try:
    connection = sql.connect(db)
    cursor = connection.cursor()
    logger.info(f"База данных {db} подключена к SQLite")
    cursor.execute(tab_telecom)
    connection.commit()
    logger.info("Таблица telecom_companies успешно добавлена в БД")
    with zipfile.ZipFile(egrul_archive, 'r') as zip:
        names = zip.namelist()
        for name in names:
            data = []
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
                try:
                    cursor.executemany(insert_telecom, data)
                    connection.commit()
                    logger.info(f"Данные файла {name} успешно добавлены в таблицу telecom_companies")
                except sql.Error as error:
                    logger.error(f"Не удалось добавить данные файла {name} в таблицу telecom_companies")
                    logger.error(f"Исключение: {error.__class__}, {error.args}")
    cursor.close()
except sql.Error as error:
    logger.critical("Не удалось добавить таблицу telecom_companies")
    logger.criticallogger.error(f"Исключение: {error.__class__}, {error.args}")
except Exception:
    logger.critical(f"Ошибка чтения архива {egrul_archive}")
finally:                    
    if (connection):
        connection.close()
        logger.info("Соединение с SQLite закрыто")