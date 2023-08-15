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

# Генерируем и добавляем серийный номер инструмента
def add_next_serial_number_to_db(connection):
    nums = get_bodys_num_from_db(connection)
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT date_part('year', CURRENT_TIMESTAMP)""")
            year = int(cursor.fetchall()[0][0] - 2000)
            temp = []
            for i in range(len(nums)):
                if nums[i][0][1:3] == str(year):
                    temp.append(nums[i][0])
            nums = temp
            if len(nums) > 0:
                last_num = str(int(nums[len(nums) - 1][-3:]) + 1)
            else:
                last_num = '001'
            
            while len(last_num) < 3:
                last_num = '0' + last_num
            next_num = 'B' + str(year) + last_num
            
            cursor.execute("""INSERT INTO instruments 
                            (serial_number, status, time_start)
                            VALUES (%s, 'in work', CURRENT_TIMESTAMP)""",
                            (next_num, ))
            return next_num
        except Exception as _ex:
            print('[INFO] Some problem in add_next_serial_number_to_db()', _ex)

# Высняем, есть ли в instruments серийный номер, котрый не укомплектован введенным телом
# Если есть -> возвращаем его, если нет -> добавляем новый номер в instruments и возвращаем
def get_next_body_num_by_section(connection, section):
    nums = get_bodys_num_from_db(connection)
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            for i in range(len(nums)):
                cursor.execute("""SELECT count(*) 
                               FROM bodys 
                               WHERE section=%s AND serial_number=%s""",
                               (section, nums[i], ))
                if cursor.fetchall()[0][0] == 0:
                    return nums[i][0]
            return add_next_serial_number_to_db(connection)
        except Exception as _ex:
            print('[INFO] Some problem in get_next_body_num_by_section()', _ex)

# Добавляем в bodys новое тело, а в bodys_list список деталей принадлежащих этому телу
def add_new_num_body(connection, serial_number, section):
    if connection.closed:
        connection = getConnection()
    with connection.cursor() as cursor:
        try:
            cursor.execute("""INSERT INTO bodys 
                           (section, serial_number, status) 
                           VALUES (%s, %s, %s)""", 
                           (section, serial_number, 'in work', ))
            cursor.execute("""SELECT id 
                           FROM bodys 
                           WHERE section=%s AND serial_number=%s""", 
                           (section, serial_number, ))
            ans = cursor.fetchall()
            id = ans[0][0]
            parts = get_bodys_parts_list_from_db(connection, section)
            print(parts)
            for i in range(len(parts)):
                if parts[i].find('W') == -1:
                    cursor.execute("""INSERT INTO bodys_list 
                                   (body_id, part_id, status) 
                                   VALUES (%s, %s, 'not started')""", 
                                   (id, parts[i], ))
                else:
                    cursor.execute("""INSERT INTO bodys_list 
                                   (body_id, part_id, status) 
                                   VALUES (%s, %s, %s)""", 
                                   (id, parts[i], 'in stock', ))
        except Exception as _ex:
            print('[INFO] Some problem in add_new_num_body()', _ex)
        
def correct_data_in_db(query, username, call, connection, bot):
    print("query =", query)
    write_query_log("query = " + str(query), connection)
    if connection.closed:
        connection = getConnection()
    if query[_ACTION] == "get":
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
                print("[INFO] Some problem with UPDATE stages - 1:", _ex)
    elif query[_ACTION] == "put":
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
                print("[INFO] Some problem with UPDATE stages - 2:", _ex)
    elif query[_ACTION] == "know":
        with connection.cursor() as cursor:
            try:
                parts = query[_PART].split('|')[1:]
                stages = query[_STAGE].split('|')[1:]
                count = query[_COUNT].split('|')[1:]
                text = ''
                for i in range(len(parts)):
                    cursor.execute("SELECT count FROM stages WHERE part_id = %s and name = %s", (parts[i], stages[i], ))
                    count = cursor.fetchone()
                    #cursor.execute("INSERT INTO log (username, action, part_id, stage_name, count) VALUES (%s, %s, %s, %s, %s)", 
                    #               (username, query[_ACTION], query[_PART], query[_STAGE], 0, ))
                    text += parts[i] + ', ' + stages[i] + ': ' + str(count[0]) + ' штук(и) в наличии\n'
                    write_log(username, query[_ACTION], parts[i], stages[i], 0, connection)
                bot.send_message(call.message.chat.id, text=text)
            except Exception as _ex:
                print("[INFO] Some problem with UPDATE stages - 3:", _ex)

    elif query[_ACTION] == "correct":
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
                print("[INFO] Some problem with UPDATE stages - 4:", _ex)

def correct_num_data_in_db(query, username, call, connection, bot):
    