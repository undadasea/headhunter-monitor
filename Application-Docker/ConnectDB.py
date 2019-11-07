""" Python script to connect and to create databases needed in PostgreSQL docker """
# TODO: check if I can delete create_user.sh
import psycopg2
import time


# forces the current thread to sleep for ... seconds
# needed in order to wait until database is started
time.sleep(12)

hostname = '172.168.0.2'
port = '5432'
username = 'postgres_docker'
password = 'dockerPass'
database = 'db_vacancies'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()
    cur.execute( "CREATE TABLE vacancies (id int, name varchar(60));")
    cur.execute( "SELECT * FROM vacancies" )
    print(cur.fetchall())

print("Using psycopg2…")
myConnection = psycopg2.connect( host=hostname, port=port, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()
