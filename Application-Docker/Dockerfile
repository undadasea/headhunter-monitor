FROM python:3

ADD ConnectDB.py /
ADD wait-for-postgres.sh /

RUN pip install psycopg2

CMD [ "python", "./ConnectDB.py" ]
