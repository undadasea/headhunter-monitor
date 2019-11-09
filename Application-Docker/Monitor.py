""" Python script to connect and to create databases needed in PostgreSQL docker """
# TODO: check if I can delete create_user.sh
import psycopg2
import time
from datetime import datetime
import http.client
import json


def getJSONresponse(connection):
    response = connection.getresponse()
    string = response.read().decode('utf-8').replace('null', '"null"')
    json_obj = json.loads(string)
    return json_obj

def selectVacancyID(cursor, id_found):
    #cursor = conn.cursor()
    cursor.execute("SELECT id FROM vacancies WHERE id = "+str(id_found)+";")
    result = cursor.fetchone()
    print(result)
    if result:
        return result[0]
    else:
        return None

def insertAddressID(cursor, vacancy):
    # check if one exists
    cursor.execute("SELECT id FROM addresses  \
                    WHERE address = "+"\'"+vacancy['address']['raw']+"\'"+";")
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE vacancies SET address_id = "+str(result[0])+
                        " WHERE id = "+str(vacancy['id'])+";")
    else:
        cursor.execute("INSERT INTO addresses(address, metro, employer_id) \
                        VALUES (\'" + vacancy['address']['raw'] + "\',"
                                "\'"+ vacancy['address']['metro'] + "\',"
                                + str(vacancy['employer']['id']) +");")

        cursor.execute("SELECT id FROM addresses  \
                        WHERE address = " + "\'"+vacancy['address']['raw']+"\';")
        result = cursor.fetchone()
        cursor.execute("UPDATE vacancies SET address_id = "+str(result[0]) +
                       " WHERE id = "+str(vacancy['id'])+";")

def insertContactID(cursor, vacancy):
    cursor.execute("SELECT id FROM contact_person  \
                    WHERE name = "+"\'"+vacancy['contacts']['name']+"\'"+";")
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE vacancies SET contact_id = "+str(result[0])+
                        " WHERE id = "+str(vacancy['id'])+";")
    else:
        cursor.execute("INSERT INTO contact_person(name, employer_id, email, phone, comment) \
                        VALUES (\'" + vacancy['contacts']['name'] + "\'," +
                                  str(vacancy['employer']['id']) + "," +
                                 "\'"+vacancy['contacts']['email'] + "\'," +
                                  str(vacancy['contacts']['phones'][0]['country']) +
                                  str(vacancy['contacts']['phones'][0]['city'])+
                                  str(vacancy['contacts']['phones'][0]['number']) + "," +
                                 "\'"+vacancy['contacts']['phones'][0]['comment'] +"\');")
        cursor.execute("SELECT id FROM contact_person  \
                        WHERE name = "+"\'"+vacancy['contacts']['name']+"\'"+";")
        result = cursor.fetchone()
        cursor.execute("UPDATE vacancies SET contact_id = "+str(result[0])+
                        " WHERE id = "+str(vacancy['id'])+";")


def insertVacancy(cursor, vacancy):
    #cursor = conn.cursor()
    cursor.execute("INSERT INTO vacancies(id, \
                                          name, \
                                          premium, \
                                          has_test, \
                                          letter_required, \
                                          type, \
                                          employer_id, \
                                          created_at, \
                                          published_at, \
                                          requirement, \
                                          responsibility, \
                                          last_update) \
                    VALUES("+str(vacancy['id'])+","+
                            "\'"+vacancy['name']+"\',"+
                             str(vacancy['premium'])+","+
                             str(vacancy['has_test'])+","+
                             str(vacancy['response_letter_required'])+","+
                        "\'"+str(vacancy['type']['id'])+"\',"+
                             str(vacancy['employer']['id'])+","+
                        "TIMESTAMP \'"+str(vacancy['created_at'])+"\',"+
                        "TIMESTAMP \'"+str(vacancy['published_at'])+"\',"+
                        "\'"+str(vacancy['snippet']['requirement'])+"\',"+
                        "\'"+str(vacancy['snippet']['responsibility'])+"\',"+
                        "TIMESTAMP \'"+str(datetime.now().isoformat())+"\');")
    # check if there's the same first
    if vacancy['address'] != "null":
        insertAddressID(cursor, vacancy)
    if vacancy['contacts'] != "null":
        insertContactID(cursor, vacancy)
    if vacancy['salary'] != "null":
        cursor.execute("UPDATE vacancies SET \
                               salary_from = "+str(vacancy['salary']['from'])+","+
                               "salary_to = "+str(vacancy['salary']['to'])+"," +
                               "currency = "+"\'"+vacancy['salary']['currency']+"\'," +
                               "gross = "+str(vacancy['salary']['gross'])+
                       " WHERE id ="+vacancy['id']+";")
    cursor.execute("SELECT * FROM vacancies;")
    print(cursor.fetchall())

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
#pages = 1
#items_per_page = 1

for page_num in range(pages):
    hh_connection.request("GET", "/vacancies?industry=7&area=2&page="+str(page_num), headers={"User-Agent":header})
    for item in range(items_per_page):
        vacancy = getJSONresponse(hh_connection)['items'][item]
        if selectVacancyID(cursor, vacancy['id']):
            cursor.execute("UPDATE vacancies SET last_update = TIMESTAMP \'"+str(datetime.now().isoformat())+"\');")
        else:
            insertVacancy(cursor, vacancy)

cursor.execute("SELECT * FROM contact_person;")
print(cursor.fetchall())

hh_connection.close()
SQL_connection.close()
