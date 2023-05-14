from datetime import datetime, timedelta
from random import randint

import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost", port="5432", database="mydb", user="admin", password="admin"
)

with conn:
    cur = conn.cursor()

    # Заполнение таблицы servers
    servers = [
        ("Server 1",),
        ("Server 2",),
        ("Server 3",),
        ("Server 4",),
        ("Server 5",),
    ]

    for srv in servers:
        cur.execute("INSERT INTO servers (srv_name) VALUES (%s)", srv)

    # Заполнение таблицы server_hdd
    server_hdd = [
        (1, "HDD 1", 45000),
        (1, "HDD 2", 55000),
        (4, "HDD 3", 50000),
        (2, "HDD 4", 55000),
        (2, "HDD 5", 60000),
        (3, "HDD 6", 120000),
        (4, "HDD 7", 70000),
        (5, "HDD 8", 60000),
    ]

    for hdd in server_hdd:
        cur.execute(
            "INSERT INTO server_hdd (srv_id, hdd_name, hdd_capacity) VALUES (%s, %s, %s)",
            hdd,
        )

    # Заполнение таблицы hdd_monitoring
    monitoring_date = datetime(2023, 5, 13)
    for hdd_id in range(1, 9):
        for i in range(30):
            used_space = randint(1, 8000)
            formatted_space = randint(1, 10000)
            cur.execute(
                "INSERT INTO hdd_monitoring (hdd_id, used_space, formatted_space, monitoring_date) VALUES (%s, %s, %s, %s)",
                (hdd_id, used_space, formatted_space, monitoring_date),
            )
            monitoring_date += timedelta(days=1)

    conn.commit()
