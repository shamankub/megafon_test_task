#!/bin/bash

# Читаем список серверов из файла
mapfile -t SERVERS < servers.txt

EMAIL="mailbox@server.ru"

SOURCE_PATH="/path/to/file.txt"

DESTINATION_PATH="/path/to/destination/"

FAILED=()

ATTACHED_FILE_NAME="/path/to/failed_$(date +"%Y-%m-%d_%H-%M").txt"

for server in "${SERVERS[@]}"
do
  # Пытаемся загрузить файл на сервер
  if ! scp "$SOURCE_PATH" user@"$server":"$DESTINATION_PATH" ; then
    # Если попытка неудачная, тогда записываем адрес сервера в список FAILED
    FAILED+=("$server")
  fi
done

# Проверяем, что список не пустой
if [ ${#FAILED[@]} -gt 0 ]; then
  # Сохраняем список серверов в файл
  printf '%s\n' "${FAILED[@]}" > $ATTACHED_FILE_NAME

  # Отправляем файл во вложении
  echo "Во вложении указан список серверов, на которые загрузка файла не удалась." | mutt -s "Ошибка выгрузки данных на сервер" -a $ATTACHED_FILE_NAME -- $EMAIL
fi