import psycopg2
import psycopg2.sql

try:
    conn = psycopg2.connect(host='127.0.0.1',
                            port='5432',
                            user='postgres',
                            password='1234',
                            database='bassoon')
    conn.autocommit = True
    section = 'BF'
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM {table}".format(table=section.lower() + '_list'))
        parts = cursor.fetchall()
        for i in range(len(parts)):
            print(parts[i][0])
except Exception as _ex:
    print('[INFO]', _ex)