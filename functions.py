from const import users_list
from const import _ACTION, _SECTION, _TYPE, _PART, _STAGE, _COUNT, _BODYNUM, _NEXT_STEP, _NEXT_PART
import psycopg2
import psycopg2.sql

######################################################################################################################################################
######################################################################################################################################################
# Подключение к базе данных
def getConnection():
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
    try:
        connection = psycopg2.connect(host=param[_HOST],
                                      port=param[_PORT],
                                      database=param[_DATABASE],
                                      user=param[_USER],
                                      password=param[_PASSWORD])
        connection.autocommit = True
        print("Successfully connected to PostgreSQL database. . .")
        return connection
    except Exception as _ex:
        print("[INFO] Some problem with connecting to PostgreSQL", _ex)

# Функция проверки допуска пользователя
def check_access(username):
    for name in users_list:
        if name == username:
            return True
    return False

# Функция проверки наличия элемента в массиве
def chek_is_element_in_arr(arr, element):
    for e in arr:
        if element == e:
            return True
    return False

# Функция генерирования строки _COUNT из массива
def gen_count_str_from_arr(arr):
    out = ""
    for part in arr:
        out += '|' + part
    return out

def get_type_message(action):
    if action == "get":
        return "Детали какого типа вы хотите взять?"
    elif action == "put":
        return "Детали какого типа вы хотите положить?"
    elif action == "know":
        return "Количество деталей какого типа вы хотите узнать?"
    elif action == "correct":
        return "Количество деталей какого тива вы хотите скорректировать?"
    return ""

def get_text_from_arrays(parts, stages, count):
    t = ''
    for i in range(len(parts)):
        t += '  ' + parts[i] + ', ' + stages[i] + ', ' + count[i] + '\n'
    return t

def get_approve_text(query):
    parts = query[_PART].split('|')[1:]
    stages = query[_STAGE].split('|')[1:]
    if query[_COUNT] == '':
        for i in range(len(stages)):
            query[_COUNT] += '|1'
    count = query[_COUNT].split('|')[1:]
    text = ''
    if query[_ACTION] == 'get':
        return 'Взять:\n' + get_text_from_arrays(parts, stages, count)
    elif query[_ACTION] == 'put':
        return 'Положить:\n' + get_text_from_arrays(parts, stages, count)
    elif query[_ACTION] == 'correct':
        return 'Установить количество:\n' + get_text_from_arrays(parts, stages, count)
    
def get_bodynum_text(query):
    parts = query[_PART].split('|')[1:]
    stages = query[_STAGE].split('|')[1:]
    text = ''
    for i in range(len(parts)):
        text += '  ' + parts[i] + ', ' + stages[i] + '\n'
    return text

def write_query_log(text, connection):
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            cursor.execute("""INSERT INTO querylog (text) VALUES (%s)""", (text, ))
        except Exception as _ex:
            print("[INFO] Some problem with INSERT INTO querylog:", _ex)

def write_log(username, action, part, stage, count, connection):
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            cursor.execute("""INSERT INTO log 
                                (username, action, part_id, stage_name, count) 
                           VALUES (%s, %s, %s, %s, %s)""", 
                               (username, action, part, stage, count, ))
        except Exception as _ex:
            print("[ERROR] Some problem with INSERT INTO log:", _ex)
            write_query_log("[ERROR] Some problem with INSERT INTO log: " 
                            + str(_ex), connection)
            
def get_parts_list_from_db(pattern, connection):
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT id 
                           FROM parts 
                           WHERE id LIKE %s""", 
                           (pattern,))
            mas = cursor.fetchall()
            return mas
        except Exception as _ex:
            print("[INFO] Some problem with SELECT FROM parts:", _ex)
            write_query_log("[INFO] Some problem with SELECT FROM parts:" 
                            + str(_ex), connection)
            return []

# Получить список деталей принадлежащих колену(b%_list)   
def get_bodys_parts_list_from_db(connection, section):
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT * FROM {table}"""
                           .format(table=section.lower() + '_list'))
            arr = cursor.fetchall()
            return arr
        except Exception as _ex:
            print('[INFO] Some problem in get_bodys_parts_list_from_db() ', _ex)
        
def get_stages_list_from_db(part, connection):
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT name 
                           FROM stages 
                           WHERE part_id = %s""", 
                           (part,))
            mas = cursor.fetchall()
            return mas
        except Exception as _ex:
            print("[INFO] Some problem with SELECT FROM stages:", _ex)
            write_query_log("[INFO] Some problem with SELECT FROM stages:" 
                            + str(_ex), connection)
            return []
        
# Получить список серийных номеров, находящихся в работе
def get_bodys_num_from_db(connection):
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT serial_number 
                           FROM instruments 
                           WHERE status='in work' 
                           ORDER BY serial_number""")
            mas = cursor.fetchall()
            return mas
        except Exception as _ex:
            print('[INFO] Some problem with SELECT FROM instruments:', _ex)
            write_query_log('[INFO] Some problem with SELECT FROM instruments:' 
                            + str(_ex), connection)
            return []

def get_bodys_num_by_section(connection, section):
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            cursor.execute('''SELECT serial_number 
                           FROM bodys 
                           WHERE section=%s AND status='in work'
                           ORDER BY serial_number''', (section, ))
            mas = cursor.fetchall()
            return mas
        except Exception as _ex:
            print('[INFO] Some problem with SELECT FROM bodys:', _ex)
            write_query_log('[INFO] Some problem with SELECT FROM bodys:' 
                            + str(_ex), connection)
            return []


        
def correct_data_in_db(query, username, call, connection, bot):
    print("query =", query)
    write_query_log("query = " + str(query), connection)
    if connection.closed:
        connection = getConnection()
    ## TYPE != num #######################################################
    ######################################################################
    if query[_TYPE] != 'num':
        if query[_ACTION] == "get":
            get_correct_in_db(query, username, call, connection, bot)
        elif query[_ACTION] == "put":
            put_correct_in_db(query, username, call, connection, bot)
        elif query[_ACTION] == "know":
            know_correct_in_db(query, username, call, connection, bot)
        elif query[_ACTION] == "correct":
            correct_correct_in_db(query, username, call, connection, bot)
    else:
        if query[_ACTION] == 'get':
            get_num_correct_in_db(query, username, call, connection, bot)
        elif query[_ACTION] == 'put':
            put_num_correct_in_db(query, username, call, connection, bot)
        elif query[_ACTION] == 'know':
            know_num_correct_in_db(query, username, call, connection, bot)
        elif query[_ACTION] == 'correct':
            correct_num_correct_in_db(query, username, call, connection, bot)

def get_correct_in_db(query, username, call, connection, bot):
    with connection.cursor() as cursor:
        try:
            parts = query[_PART].split('|')[1:]
            stages = query[_STAGE].split('|')[1:]
            count = query[_COUNT].split('|')[1:]
            for i in range(len(parts)):
                cursor.execute("UPDATE stages SET count = count - %s WHERE part_id = %s and name = %s",
                        (int(count[i]), parts[i], stages[i],))
                #cursor.execute("INSERT INTO log (username, action, part_id, stage_name, count) VALUES (%s, %s, %s, %s, %s)", 
                #               (username, query[_ACTION], query[_PART], query[_STAGE], query[_COUNT], ))
                write_log(username, query[_ACTION], parts[i], stages[i], count[i], connection)
            bot.send_message(call.message.chat.id, text=call.message.text[call.message.text.index(':') + 2:])
        except Exception as _ex:
            print("[INFO] Some problem with UPDATE stages in get_correct_in_db:", _ex)

def put_correct_in_db(query, username, call, connection, bot):
    with connection.cursor() as cursor:
        try:
            parts = query[_PART].split('|')[1:]
            stages = query[_STAGE].split('|')[1:]
            count = query[_COUNT].split('|')[1:]
            for i in range(len(parts)):
                cursor.execute("UPDATE stages SET count = count + %s WHERE part_id = %s and name = %s",
                        (int(count[i]), parts[i], stages[i],))
                #cursor.execute("INSERT INTO log (username, action, part_id, stage_name, count) VALUES (%s, %s, %s, %s, %s)", 
                #               (username, query[_ACTION], query[_PART], query[_STAGE], query[_COUNT], ))
                write_log(username, query[_ACTION], parts[i], stages[i], count[i], connection)
            bot.send_message(call.message.chat.id, text=call.message.text[call.message.text.index(':') + 2:])
        except Exception as _ex:
            print("[INFO] Some problem with UPDATE stages in put_correct_in_db:", _ex)

def know_correct_in_db(query, username, call, connection, bot):
    with connection.cursor() as cursor:
        try:
            parts = query[_PART].split('|')[1:]
            text = ''
            for i in range(len(parts)):
                cursor.execute('''SELECT name, count 
                               FROM stages 
                               WHERE part_id = %s''', 
                               (parts[i], ))
                mas = cursor.fetchall()
                for j in range(len(mas)):
                    text += parts[i] + ', ' + str(mas[j][0]) + ': ' + str(mas[j][1]) + ' штук(и) в наличии\n'
                    write_log(username, query[_ACTION], parts[i], str(mas[j][0]), 0, connection)
                text += '\n'
            bot.send_message(call.message.chat.id, text=text)
        except Exception as _ex:
            print("[INFO] Some problem with UPDATE stages in know_correct_in_db:", _ex)

def correct_correct_in_db(query, username, call, connection, bot):
    with connection.cursor() as cursor:
        try:
            parts = query[_PART].split('|')[1:]
            stages = query[_STAGE].split('|')[1:]
            count = query[_COUNT].split('|')[1:]
            for i in range(len(parts)):
                cursor.execute("UPDATE stages SET count = %s WHERE part_id = %s and name = %s", 
                            (int(count[i]), parts[i], stages[i],))
                #cursor.execute("INSERT INTO log (username, action, part_id, stage_name, count) VALUES (%s, %s, %s, %s, %s)", 
                #               (username, query[_ACTION], query[_PART], query[_STAGE], query[_COUNT], ))
                write_log(username, query[_ACTION], parts[i], stages[i], count[i], connection)
            bot.send_message(call.message.chat.id, text=call.message.text[call.message.text.index(':') + 2:])
        except Exception as _ex:
            print("[INFO] Some problem with UPDATE stages in correct_correct_in_db:", _ex)

def get_num_correct_in_db(query, username, call, connection, bot):
    with connection.cursor() as cursor:
        try:
            parts = query[_PART].split('|')[1:]
            stages = query[_STAGE].split('|')[1:]
            cursor.execute('''SELECT id 
                           FROM bodys 
                           WHERE serial_number=%s AND section=%s''', 
                           (query[_BODYNUM], query[_SECTION], ))
            id = cursor.fetchall()[0][0]
            for i in range(len(parts)):
                cursor.execute('''UPDATE bodys_list
                               SET status='in work'
                               WHERE part_id=%s AND body_id=%s''', 
                               (parts[i], id, ))
                write_log(username, query[_ACTION], parts[i], stages[i], query[_BODYNUM], connection)
        except Exception as _ex:
            print('[INFO] Some problem with UPDATE stages in get_num_correct_in_db')

def put_num_correct_in_db(query, username, call, connection, bot):
    with connection.cursor() as cursor:
        try:
            parts = query[_PART].split('|')[1:]
            stages = query[_STAGE].split('|')[1:]
            cursor.execute('''SELECT id 
                            FROM bodys 
                            WHERE serial_number=%s AND section=%s''', 
                            (query[_BODYNUM], query[_SECTION], ))
            id = cursor.fetchall()[0][0]
            for i in range(len(parts)):
                cursor.execute('''UPDATE bodys_list 
                               SET status='in stock', stage_name=%s
                               WHERE part_id=%s AND body_id=%s''',
                               (stages[i], parts[i], id, ))
                write_log(username, query[_ACTION], parts[i], stages[i], query[_BODYNUM], connection)
        except Exception as _ex:
            print('[INFO] Some problem with UPDATE stages in put_num_correct_in_db')

def know_num_correct_in_db(query, username, call, connection, bot):
    with connection.cursor() as cursor:
        try:
            parts = query[_PART].split('|')[1:]
            stages = query[_STAGE].split('|')[1:]
            cursor.execute('''SELECT id 
                           FROM bodys
                           WHERE serial_number=%s AND section=%s''',
                           (query[_BODYNUM], query[_SECTION], ))
            id = cursor.fetchall()[0][0]
            text = ''
            for i in range(len(parts)):
                cursor.execute('''SELECT stage_name, status 
                               FROM bodys_list 
                               WHERE body_id=%s AND part_id=%s''',
                               (id, parts[i], ))
                mas = cursor.fetchall()
                stage = str(mas[0][0])
                status = str(mas[0][1])
                text += parts[i]
                if status == 'not started':
                    text += ', ' + 'не запущен в работу'
                elif status == 'in work':
                    text += ', ' + stage + ', ' + 'в работе'
                elif status == 'in stock':
                    text += ', ' + stage + ', ' + 'в наличии на складе'
                text += '\n'
                #write_log(username, query[_ACTION], parts[i], stages[i], query[_BODYNUM], connection)
            bot.send_message(call.message.chat.id, text=text)
        except Exception as _ex:
            print('[INFO] Some problem with UPDATE stages in know_num_correct_in_db')

def correct_num_correct_in_db(query, username, call, connection, bot):
    try:
        parts = query[_PART].split('|')[1:]
        stages = query[_STAGE].split('|')[1:]
    except Exception as _ex:
        print('[INFO] Some problem with UPDATE stages in correct_num_correct_in_db')