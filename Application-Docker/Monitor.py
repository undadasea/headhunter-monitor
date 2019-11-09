""" Python script to connect and to create databases needed in PostgreSQL docker """
# TODO: check if I can delete create_user.sh
import psycopg2
import pytz
import time
from datetime import datetime, timedelta
import http.client
import json


def getJSONresponse(connection):
    response = connection.getresponse()
    string = response.read().decode('utf-8').replace('null', '"null"')
    json_obj = json.loads(string)
    return json_obj

def getTime():
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Europe/Moscow"))
    print("in func: ", pst_now)
    print("in func iso:", pst_now.isoformat())
    return pst_now

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
    result = cursor.fetchall()
    if result == []:
        cursor.execute("INSERT INTO addresses(address, employer_id) \
                        VALUES (\'" + vacancy['address']['raw'] + "\',"
                                + str(vacancy['employer']['id']) +");")

        cursor.execute("SELECT id FROM addresses  \
                        WHERE address = " + "\'"+vacancy['address']['raw']+"\';")
        result = cursor.fetchall()

        if vacancy['address']['metro'] != "null":
            cursor.execute("UPDATE addresses SET metro = " +
                      "\'"+ vacancy['address']['metro']['station_name'] + "\' "+
                      "WHERE id = "+ str(result[0][0]) +";")

    cursor.execute("UPDATE vacancies SET address_id = "+str(result[0][0])+
                    " WHERE id = "+str(vacancy['id'])+";")
    # cursor.execute("UPDATE employers SET address_id = "+str(result[0][0])+
    #                 " WHERE id = "+str(vacancy['employer']['id'])+";")

def insertContactID(cursor, vacancy):
    cursor.execute("SELECT id FROM contact_person  \
                    WHERE name = "+"\'"+vacancy['contacts']['name']+"\'"+";")
    result = cursor.fetchall()
    if result == []:
        cursor.execute("INSERT INTO contact_person(name, employer_id, email) \
                        VALUES (\'" + vacancy['contacts']['name'] + "\'," +
                                  str(vacancy['employer']['id']) + "," +
                                 "\'"+vacancy['contacts']['email'] + "\');")

        cursor.execute("SELECT id FROM contact_person  \
                        WHERE name = "+"\'"+vacancy['contacts']['name']+"\'"+";")
        result = cursor.fetchall()
        print("result = ", result)

        if vacancy['contacts']['phones'] != []:
            cursor.execute("UPDATE contact_person \
                            SET phone = "+str(vacancy['contacts']['phones'][0]['country'])+
                                          str(vacancy['contacts']['phones'][0]['city'])+
                                          str(vacancy['contacts']['phones'][0]['number']) + ", \
                                comment = \'"+(vacancy['contacts']['phones'][0]['comment'])+"\' "+
                            "WHERE id = "+str(result[0][0])+";")

    cursor.execute("UPDATE vacancies SET contact_id = "+str(result[0][0])+
                    " WHERE id = "+str(vacancy['id'])+";")
    # cursor.execute("UPDATE employers SET contact_id = "+str(result[0][0])+
    #                 " WHERE id = "+str(vacancy['employer']['id'])+";")


def insertVacancy(cursor, vacancy):
    #cursor = conn.cursor()
    print("in insert: ", vacancy)
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
                        "TIMESTAMP \'"+str(getTime().isoformat())+"\');")
    cursor.execute("INSERT INTO employers(id, name) VALUES("+str(vacancy['employer']['id'])+",\'"+str(vacancy['employer']['name'])+"\') "+
                    "ON CONFLICT ON CONSTRAINT id_constr DO NOTHING;")
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

# def updateEmployers(cursor, hh_connection):
#     cursor.execute("SELECT employer_id FROM vacancies;")
#     print(cursor.fetchone())
#     for emploer_id in cursor:
#         hh_connection.request("GET", "/vacancies?employers?id="+str(employer_id), headers={"User-Agent":header})
#         employer = getJSONresponse(hh_connection)
#         #check if there's a record already
#         cursor.execute("SELECT id FROM employers  \
#                         WHERE id = " + str(emploer_id) +";")
#         result = cursor.fetchone()
#         if not result:
#             #cursor.execute("INSERT INTO employers VALUES()")
#             pass


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
pages = 10
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

cursor.execute("SELECT * FROM contact_person;")
print("contact_person: ", cursor.fetchall())
cursor.execute("SELECT * FROM employers;")
print("employers: ", cursor.fetchall())
cursor.execute("SELECT * FROM vacancies;")
print("vac: ", cursor.fetchall())

hh_connection.close()
SQL_connection.close()
