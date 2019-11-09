""" Python script to connect to database in PostgreSQL docker """

import psycopg2
import pytz
import time
from datetime import datetime, timedelta
import http.client
import json

from parse import selectVacancyID, insertVacancy, insertAddress, insertContact, getTime

def getJSONresponse(connection):
    response = connection.getresponse()
    string = response.read().decode('utf-8').replace('null', '"null"')
    json_obj = json.loads(string)
    return json_obj

# forces the current thread to sleep for ... seconds
# needed in order to wait until database is started
time.sleep(12)


hostname = '172.168.0.2'
port = '5432'
username = 'postgres_docker'
password = 'dockerPass'
database = 'db_vacancies'

header = "Python/3.7 (GNU/Linux bionic) valeriatazh@gmail.com"

SQL_connection = psycopg2.connect( host=hostname, port=port, user=username, password=password, dbname=database )
SQL_connection.autocommit = True
cursor = SQL_connection.cursor()
hh_connection = http.client.HTTPSConnection("api.hh.ru")

hh_connection.request("GET", "/vacancies?industry=7&area=2&", headers={"User-Agent":header})
json_obj = getJSONresponse(hh_connection)
pages = int(json_obj['pages'])
items_per_page = int(json_obj['per_page'])

#for testing purposes
#pages = 10
#items_per_page = 1

for page_num in range(pages):
    hh_connection.request("GET", "/vacancies?industry=7&area=2&page="+str(page_num), headers={"User-Agent":header})
    vacancies = getJSONresponse(hh_connection)['items']
    for item in range(items_per_page):
        vacancy = vacancies[item]
        if selectVacancyID(cursor, vacancy['id']):
            cursor.execute("UPDATE vacancies SET last_update = TIMESTAMP \'"+str(getTime().isoformat())+"\', " +
                                                 "type = \'open\';")
        else:
            insertVacancy(cursor, vacancy)

yesterday = getTime() - timedelta(days=1)
cursor.execute("UPDATE vacancies SET type = \'close\' WHERE id = ANY(SELECT id FROM vacancies WHERE last_update < TIMESTAMP \'"+str(yesterday.isoformat())+"\')")

hh_connection.close()
SQL_connection.close()
