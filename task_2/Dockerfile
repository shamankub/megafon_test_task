FROM python:3.9.7
WORKDIR /app
RUN apt-get update && apt-get install -y postgresql-client
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x wait-for-postgres.sh