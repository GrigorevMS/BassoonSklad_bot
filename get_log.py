import telebot
import psycopg2
import os
import time

try:
    param = []
    
    _HOST = 0
    _PORT = 1
    _DATABASE = 2
    _USER= 3
    _PASSWORD = 4
    
    with open("database_settings.txt", 'r') as fin:
        param = fin.readlines()
        for i in range(len(param)):
            param[i] = param[i][param[i].index('=')+1:-1]
            
    connection = psycopg2.connect(host=param[_HOST],
                                   port=param[_PORT],
                                   database=param[_DATABASE],
                                   user=param[_USER],
                                   password=param[_PASSWORD])
    connection.autocommit = True
    print("Successfully connected to PostgreSQL database . . .")
except Exception as _ex:
    print("[INFO] Some problem with connecting to PostgreSQL", _ex)

print("get_log.py is running . . .")
if not connection.closed:
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT time, username, action, part_id, stage_name, count FROM log ORDER BY time")
            fout = open("log.txt", 'w')
            for line in cursor.fetchall():
                fout.write('* ' + str(line[0]) + " - " + line[1] + " | " + line[2] + " | " + line[3] + " | " + line[4] + " | " + str(line[5]) + '\n\n')
            fout.close()
        except Exception as _ex:
            print("[INFO] Some problem with SELECT FROM querylog", _ex)
    connection.close()
    print("get_log.py finished . . .")
