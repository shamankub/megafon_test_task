## Задание №1

### Описание:
* Скрипт получает на вход файл `servers.txt` со списком IP-адресов и отправляет письмо, во вложении которого будет файл со списком серверов, на которые не удалось выгрузить данные.
* Для работы скрипта необходим пакет `mutt`, файл конфигурации для `mail.ru` находится в файле `mutt.zip`. 
Установка `apt-get install mutt`
* Настройки для `Cron`:
`"0 9-18 * * 1-5 /path/to/file_transfer.sh"` - выполнение по будням с 9 до 18.
`"0 * * * 1-5 /path/to/file_transfer.sh"` - выполнение по будням ежечасно.

### Список файлов:
1. `file_transfer.sh` - скрипт на bash.
2. `random_ip_list_create.py` - скрипт на Python для генерации 500 случайных IP-адресов.
3. `servers.txt` - список сгенерированных IP-адресов.
4. `mutt.zip` - файлы конфигурации для пакета mutt.



## Задание №2

### Описание:
Создаётся 2 docker контейнера: 
* скрипт Python. 
* БД (PostgreSQL).

Алгоритм взаимодействия:
* Скрипт каждую минуту отправляет данные в БД cо сгенерированными данными. 
* Логирует свои действия.
* При достижении в таблице БД 30 строк, таблица должна очищаться и вновь пришедшие данные должны быть записаны 1й строчкой. 

### Список файлов:
1. `app.py` - скрипт на Python для добавления данных в таблицу.
2. `wait-for-postgres.sh` - скрипт на bash для ожидания ответа от БД PostgreSQL.
3. `Dockerfile` - Docker-файл для создания контейнера с Python.
4. `docker-compose.yml` - создание контейнеров: `app` (скрипт Python), `db` (БД PostgreSQL).



## Задание №3

### PL/SQL

#### a. Вывести серверы, суммарная емкость накопителей которых больше 110 ТБ и менее 130 ТБ. Без использования подзапросов.

```sql
SELECT s.srv_name, SUM(h.hdd_capacity) AS total_capacity
FROM servers s
JOIN server_hdd h ON s.srv_id = h.srv_id
GROUP BY s.srv_name
HAVING SUM(h.hdd_capacity) > 110000 AND SUM(h.hdd_capacity) < 130000
ORDER BY s.srv_name;
```

#### b. Вследствие ошибки в таблице server_hdd появились дубли строк. Предложите вариант удаления дубликатов, оставив только уникальные строки.
* Удаление из выборки SELECT:
```sql
SELECT DISTINCT * FROM server_hdd;
```

* Удаление из таблицы:
```sql
DELETE FROM server_hdd
WHERE hdd_id not in
    (SELECT MAX(hdd_id)
     FROM server_hdd
     GROUP BY srv_id, hdd_name, hdd_capacity);
```
#### c. Какими средствами СУБД Oracle Вы в дальнейшем предотвратили бы появления дубликатов строк?
Для предотвращения появления дубликатов строк можно использовать уникальные индексы.
```sql
CREATE UNIQUE INDEX idx_server_hdd ON server_hdd(srv_id, hdd_name);
```
#### d. Вывести изменение занятой емкости на самых больших дисках каждого сервера в формате: Имя сервера, Имя диска, Общая емкость диска, Предыдущая занятая емкость, Текущая занятая емкость диска, Дата мониторинга. Не более 10 строк на каждый диск.
```sql
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
```

### Список файлов:
1. `1_create_tables.py` - скрипт для создания таблиц.
2. `2_insert_data.py` - скрипт для заполнения таблиц данными.
3. `3_get_all_data.py` - скрипт для получения всех данных из таблиц (результат записывается в каталог `tables`).
4. `4_task_a.py` - скрипт, выполняющий запрос из задания `a` (результат записывается в каталог `results`).
5. `5_task_d.py` - скрипт, выполняющий запрос из задания `d` (результат записывается в каталог `results`).
6. `docker-compose.yml` - создание контейнера `db` (БД PostgreSQL).

### !!!!!ВАЖНО!!!!! Из-за нехватки места на /root разделе, не было возможности создать контейнер со свежей версией Oracle, поэтому задание было выполнено в PostgreSQL. Исходя из документации, эти запросы должны выполняться и в Oracle. 
