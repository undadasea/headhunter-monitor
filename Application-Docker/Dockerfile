FROM python:3

ADD Application-Docker/Monitor.py /
ADD libs/parse.py /
ADD libs/category.py /

RUN pip install psycopg2
RUN pip install pytz

CMD [ "python", "./Monitor.py" ]
