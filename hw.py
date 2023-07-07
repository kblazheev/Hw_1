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
    with zipfile.ZipFile(okved_archive, 'r') as zip:
        with zip.open(okved_file) as file:
            okved_df = pd.read_json(file)
    logger.info(f"Данные ОКВЭД успешно загружены из архива {egrul_archive}")
    try:
        connection = sql.connect(db)
        cursor = connection.cursor()
        logger.info(f"База данных {db} подключена к SQLite")
        cursor.execute(tab_okved)
        connection.commit()
        logger.info("Таблица okved успешно добавлена в БД")
        data = []
        for index, row in okved_df.iterrows():
            data.append(row)
        cursor.executemany(insert_okved, data)
        connection.commit()
        logger.info("Данные успешно добавлены в таблицу okved")
        cursor.close()
    except sql.Error as error:
        logger.error("Не удалось вставить данные в таблицу okved")
        logger.error(f"Исключение: {error.__class__}, {error.args}")
    finally:
        if (connection):
            connection.close()
            logger.info("Соединение с SQLite закрыто")
except Exception:
    logger.critical(f"Ошибка чтения архива {egrul_archive}")