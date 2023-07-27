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

print("get_querylog.py is running . . .")
if not connection.closed:
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT time, text FROM querylog ORDER BY time")
            fout = open("querylog.txt", 'w')
            fout.write("""users_list = ["m4dw4ve", "easywiner1", "Ashurrat", "moryachyo", "SMashina", "satansmarshmallow", "MVikha"]""" + '\n\n')
            for line in cursor.fetchall():
                fout.write('* ' + str(line[0]) + " - " + line[1] + '\n\n')
            fout.close()
        except Exception as _ex:
            print("[INFO] Some problem with SELECT FROM querylog", _ex)
    connection.close()
    print("get_querylog.py finished . . .")
