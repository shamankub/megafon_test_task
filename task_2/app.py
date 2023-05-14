import datetime
import logging
import random
import string
import time

import psycopg2

# Настройка логирования
logging.basicConfig(
    filename="db.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


# Функция для обрезки строки до указанной длины
def truncate(s, length):
    if len(s) <= length:
        return s
    else:
        return s[: length - 3] + "..."


# Функция для генерации произвольной строки
def generate_random_string(length):
    letters = string.ascii_lowercase
    result = "".join([random.choice(letters) for _ in range(length)])
    return result


# Функция для записи данных в БД
def write_data(conn):
    data = generate_random_string(40)
    date = datetime.datetime.now()

    # Запись данных в таблицу
    cur = conn.cursor()
    cur.execute("INSERT INTO mytable (data, date) VALUES (%s, %s)", (data, date))
    conn.commit()

    logging.info(f"Добавление данных -> '{truncate(data, 30)}'")


# Функция для очистки таблицы
def clear_table(conn):
    # Подсчёт количества записей в таблице
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM mytable")
    count = cur.fetchone()[0]

    if count >= 30:
        # Удаление всех записей в таблице
        cur.execute("DELETE FROM mytable")
        conn.commit()

        # Обнуление счётчика SERIAL
        cur.execute("ALTER SEQUENCE mytable_id_seq RESTART WITH 1")
        conn.commit()

        logging.info("Таблица была очищена.")


# Установка соединения с БД
conn = psycopg2.connect(
    host="db",
    port="5432",
    database="mydatabase",
    user="admin",
    password="admin",
)

with conn:
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mytable 
        (
            id SERIAL PRIMARY KEY,
            data TEXT NOT NULL,
            date TIMESTAMP NOT NULL
        );
        """
    )
    conn.commit()

    # Цикл для генерации данных и очистки таблицы
    while True:
        write_data(conn)

        # Задержка на 1 минуту
        time.sleep(60)

        clear_table(conn)
