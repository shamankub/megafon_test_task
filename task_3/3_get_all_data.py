import psycopg2
from tabulate import tabulate

# Указываем данные для подключения
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydb",
    user="admin",
    password="admin",
)

with conn:
    cur = conn.cursor()

    # Получаем данные таблицы servers
    cur.execute("SELECT * FROM servers")
    servers = cur.fetchall()

    # Записываем данные таблицы servers в файл servers.txt
    with open("task_3/tables/servers.txt", "w") as f:
        f.write(tabulate(servers, headers=["srv_id", "srv_name"]))

    # Получаем данные таблицы server_hdd
    cur.execute("SELECT * FROM server_hdd")
    server_hdd = cur.fetchall()

    # Записываем данные таблицы server_hdd в файл server_hdd.txt
    with open("task_3/tables/server_hdd.txt", "w") as f:
        f.write(
            tabulate(
                server_hdd, headers=["hdd_id", "srv_id", "hdd_name", "hdd_capacity"]
            )
        )

    # Получаем данные таблицы hdd_monitoring
    cur.execute("SELECT * FROM hdd_monitoring")
    hdd_monitoring = cur.fetchall()

    # Записываем данные таблицы hdd_monitoring в файл hdd_monitoring.txt
    with open("task_3/tables/hdd_monitoring.txt", "w") as f:
        f.write(
            tabulate(
                hdd_monitoring,
                headers=["hdd_id", "used_space", "formatted_space", "monitoring_date"],
            )
        )
