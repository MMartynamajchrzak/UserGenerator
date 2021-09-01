FROM python:3.9.6

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY wait-for-postgres.sh /wait-for-postgres.sh

RUN chmod +x wait-for-postgres.sh

WORKDIR /app
