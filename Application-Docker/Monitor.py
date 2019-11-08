""" Python script to connect and to create databases needed in PostgreSQL docker """
# TODO: check if I can delete create_user.sh
import psycopg2
import time
import http.client
import json


def getJSONresponse(connection):
    response = connection.getresponse()
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    return json_obj

def selectVacancyID(conn, id_found):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM vacancies WHERE id = "+str(id_found)+";")
    result = cursor.fetchone()
    print(result)
    if result:
        return result[0]
    else:
        return None

def insertVacancy(conn, vacancy):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vacancies(id, name) VALUES("+str(vacancy['id'])+","+"\'"+vacancy['name']+"\'"+");")

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
hh_connection = http.client.HTTPSConnection("api.hh.ru")

hh_connection.request("GET", "/vacancies?industry=7&area=2&", headers={"User-Agent":header})
json_obj = getJSONresponse(hh_connection)
pages = int(json_obj['pages'])
items_per_page = int(json_obj['per_page'])
print("pages=", pages)

pages = 1
item = 1

for page_num in range(pages):
    hh_connection.request("GET", "/vacancies?industry=7&area=2&page="+str(page_num), headers={"User-Agent":header})
    for item in range(items_per_page):
        vacancy = getJSONresponse(hh_connection)['items'][item]
        if selectVacancyID(SQL_connection, vacancy['id']):
            print("vacancy ", vacancy['id'], " found")
            pass
            #update
        else:
            print("no vacancy ", vacancy['id'], " found")
            insertVacancy(SQL_connection, vacancy)

cursor = SQL_connection.cursor()
cursor.execute("SELECT * FROM vacancies;")
print(cursor.fetchall())

hh_connection.close()
SQL_connection.close()
