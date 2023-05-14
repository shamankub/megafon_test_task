import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost", port="5432", database="mydb", user="admin", password="admin"
)

with conn:
    cur = conn.cursor()
    
    # Создаем таблицу servers
    cur.execute(
        """
        CREATE TABLE servers (
            srv_id SERIAL PRIMARY KEY,
            srv_name VARCHAR(100) NOT NULL
        )
    """
    )

    # Создаем таблицу server_hdd
    cur.execute(
        """
        CREATE TABLE server_hdd (
            hdd_id SERIAL PRIMARY KEY,
            srv_id INTEGER REFERENCES servers(srv_id),
            hdd_name VARCHAR(100) NOT NULL,
            hdd_capacity NUMERIC NOT NULL
        )
    """
    )

    # Создаем таблицу hdd_monitoring
    cur.execute(
        """
        CREATE TABLE hdd_monitoring (
            hdd_id INTEGER REFERENCES server_hdd(hdd_id),
            used_space NUMERIC NOT NULL,
            formatted_space NUMERIC NOT NULL,
            monitoring_date DATE NOT NULL,
            PRIMARY KEY (hdd_id, monitoring_date)
        )
    """
    )

    conn.commit()
