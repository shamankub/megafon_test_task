import random

# Создаём файл со списком серверов
with open("servers.txt", "w") as file:
    for i in range(500):
        ip_address = ".".join([str(random.randint(0, 255)) for _ in range(4)])
        file.write(f"{ip_address}\n")
