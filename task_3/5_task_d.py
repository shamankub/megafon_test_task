import psycopg2
from tabulate import tabulate

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost", port="5432", database="mydb", user="admin", password="admin"
)

with conn:
    cur = conn.cursor()

    cur.execute(
        """
        SELECT sub.srv_name, sub.hdd_name, sub.hdd_capacity, 
        LAG(sub.used_space) OVER (PARTITION BY sub.srv_id, sub.hdd_id ORDER BY sub.monitoring_date) as prev_used_space,
        sub.used_space, sub.monitoring_date
        FROM (
        SELECT s.srv_id, s.srv_name, h.hdd_id, h.hdd_name, h.hdd_capacity, m.used_space, m.monitoring_date,
                ROW_NUMBER() OVER (PARTITION BY s.srv_id, h.hdd_id ORDER BY m.monitoring_date DESC) as row_num
        FROM servers s
        JOIN server_hdd h ON s.srv_id = h.srv_id
        JOIN hdd_monitoring m ON h.hdd_id = m.hdd_id
        WHERE m.used_space IS NOT NULL
            AND h.hdd_capacity = (
                SELECT MAX(hdd_capacity) 
                FROM server_hdd 
                WHERE srv_id = s.srv_id
            )
        ) sub
        WHERE sub.row_num <= 10
        ORDER BY sub.srv_id, sub.hdd_capacity, sub.monitoring_date;

    """
    )

    # Получение результатов запроса
    rows = cur.fetchall()

    # Вывод результатов в файл
    with open("task_3/results/task_d.txt", "w") as f:
        f.write(
            tabulate(
                rows,
                headers=[
                    "Server Name",
                    "HDD Name",
                    "HDD Capacity",
                    "Previous Used Space",
                    "Used Space",
                    "Monitoring Date",
                ],
            )
        )
