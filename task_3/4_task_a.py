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
        SELECT s.srv_name, SUM(h.hdd_capacity) AS total_capacity
        FROM servers s
        JOIN server_hdd h ON s.srv_id = h.srv_id
        GROUP BY s.srv_name
        HAVING SUM(h.hdd_capacity) > 110000 AND SUM(h.hdd_capacity) < 130000
        ORDER BY s.srv_name;
    """
    )

    # Получение результатов запроса
    rows = cur.fetchall()

    # Вывод результатов в файл
    with open("task_3/results/task_a.txt", "w") as f:
        f.write(
            tabulate(
                rows,
                headers=["Server Name", "Total Capacity"],
            )
        )
