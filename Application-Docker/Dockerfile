FROM python:3

ADD Monitor.py /

RUN pip install psycopg2
RUN pip install pytz

CMD [ "python", "./Monitor.py" ]
