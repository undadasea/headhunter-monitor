import psycopg2
import pytz
from category import category, jobs, developer_experience
from datetime import datetime

def getTime():
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Europe/Moscow"))
    return pst_now


def selectVacancyID(cursor, id_found):
    cursor.execute("SELECT id FROM vacancies WHERE id = "+str(id_found)+";")
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def insertAddress(cursor, vacancy):
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


def insertContact(cursor, vacancy):
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

        if vacancy['contacts']['phones'] != []:
            cursor.execute("UPDATE contact_person \
                            SET phone = "+str(vacancy['contacts']['phones'][0]['country'])+
                                          str(vacancy['contacts']['phones'][0]['city'])+
                                          str(vacancy['contacts']['phones'][0]['number']) + ", \
                                comment = \'"+(vacancy['contacts']['phones'][0]['comment'])+"\' "+
                            "WHERE id = "+str(result[0][0])+";")

    cursor.execute("UPDATE vacancies SET contact_id = "+str(result[0][0])+
                    " WHERE id = "+str(vacancy['id'])+";")


def insertVacancy(cursor, vacancy):
    try:
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
                                              last_update, \
                                              job, \
                                              developer_experience) \
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
                  "TIMESTAMP \'"+str(getTime().isoformat())+"\'," +
                            "\'"+str(category(jobs, vacancy))+"\', "+
                            "\'"+str(category(developer_experience, vacancy))+"\');")
        cursor.execute("INSERT INTO employers(id, name) VALUES("+str(vacancy['employer']['id'])+",\'"+str(vacancy['employer']['name'])+"\') "+
                        "ON CONFLICT ON CONSTRAINT id_constr DO NOTHING;")
    # check if there's the same first
        if vacancy['address'] != "null":
            insertAddress(cursor, vacancy)
        if vacancy['contacts'] != "null":
            insertContact(cursor, vacancy)
        if vacancy['salary'] != "null":
            cursor.execute("UPDATE vacancies SET \
                                   salary_from = "+str(vacancy['salary']['from'])+","+
                                   "salary_to = "+str(vacancy['salary']['to'])+"," +
                                   "currency = "+"\'"+vacancy['salary']['currency']+"\'," +
                                   "gross = "+str(vacancy['salary']['gross'])+
                           " WHERE id ="+vacancy['id']+";")
    except KeyError:
        print("Vacancy wasn't inserted")
