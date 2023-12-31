from const import users_list, first_body_num_stage, body_num_stages, _ACTION, _SECTION, _TYPE, _PART, _STAGE, _COUNT, _BODYNUM, _NEXT_STEP, _NEXT_PART
import functions as f
import keyboards as k
import os

### start, help, finish ##############################################################################################################################
######################################################################################################################################################
def start_handler(query_list, message, bot, connection):
    ind = users_list.index(message.chat.username)
    try:
        bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1, text="Отмена")
    except:
        pass
    bot.delete_message(message.chat.id, message.message_id)
    query_list[ind] = ["", "", "", "", "", "", "", "", 0]
    query_list[ind][_NEXT_STEP] = "ACTION"
    bot.send_message(message.from_user.id, text="Привет, что вы хотите сделать?", reply_markup=k.get_activity_keyboard())
    return query_list

def help_handler(query_list, message, bot, connection, bot_help_text):
    ind = users_list.index(message.chat.username)
    try:
        bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1, text="Отмена")
    except:
        pass
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.from_user.id, bot_help_text)
    with open('stage_diagram.png', 'rb') as photo:
        bot.send_message(message.from_user.id, "Диаграмма этапов:")
        bot.send_photo(message.from_user.id, photo)
    return query_list

def finish_handler(query_list, message, bot, connection):
    ind = users_list.index(message.chat.username)
    try:
        bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1, text="Отмена")
    except:
        pass
    bot.delete_message(message.chat.id, message.message_id)
    query_list[ind] = ["", "", "", "", "", "", "", "", 0]
    print("finish =", query_list)
    f.write_query_log("finish = " + str(query_list), connection)
    return query_list

### ACTION -> get, put, know, correct, getlist, getlog ###############################################################################################
######################################################################################################################################################
def get_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_ACTION] = "get"
    query_list[ind][_NEXT_STEP] = "SECTION"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, 
                     text="Детали из какой группы вы хотите взять?", 
                     reply_markup=k.get_section_keyboard())
    return query_list

def put_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_ACTION] = "put"
    query_list[ind][_NEXT_STEP] = "SECTION"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, text="Детали из какой группы вы хотите положить?", reply_markup=k.get_section_keyboard())
    return query_list

def know_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_ACTION] = "know"
    query_list[ind][_NEXT_STEP] = "SECTION"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, text="Количество деталей из какой группы вы хотите узнать?", reply_markup=k.get_section_keyboard())
    return query_list

def correct_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_ACTION] = "correct"
    query_list[ind][_NEXT_STEP] = "SECTION"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, text="Количество деталей из какой группы вы хотите скорректировать?", reply_markup=k.get_section_keyboard())
    return query_list

def getlist_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id - 1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id - 1, text="Отмена")
    except:
        pass
    os.system('python gen_vedomost.py')
    with open('BassoonPartsList.xls', 'rb') as f1:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_document(chat_id=call.message.chat.id, document=f1)
    os.remove('BassoonPartsList.xls')

    f.write_query_log("getlist by 'gen_vedomost.py'", connection)
    f.write_log(call.message.chat.username, "getlist", "-", "-", "0", connection)
    return query_list

def getlog_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id - 1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id - 1, text="Отмена")
    except:
        pass
    
    os.system('python get_querylog.py')
    os.system('python get_log.py')
    with open('querylog.txt', 'rb') as f1:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id, text = 'Логи')
        bot.send_document(chat_id=call.message.chat.id, document=f1)
    os.remove('querylog.txt')
    
    with open('log.txt', 'rb') as f2:
        bot.send_document(chat_id=call.message.chat.id, document=f2)
    os.remove('log.txt')

    f.write_query_log("getlog by 'get_querylog.py' and 'get_log.py'", connection)
    f.write_log(call.message.chat.username, "getlog", "-", "-", "0", connection)
    return query_list

### SECTION -> BF, BS, BB, BR, BCup, STAND ###########################################################################################################
######################################################################################################################################################
def bf_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_SECTION] = "BF"
    query_list[ind][_NEXT_STEP] = "TYPE"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, text=f.get_type_message(query_list[ind][_ACTION]), reply_markup=k.get_type_keyboard())
    return query_list

def bs_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_SECTION] = "BS"
    query_list[ind][_NEXT_STEP] = "TYPE"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, text=f.get_type_message(query_list[ind][_ACTION]), reply_markup=k.get_type_keyboard())
    return query_list

def bb_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_SECTION] = "BB"
    query_list[ind][_NEXT_STEP] = "TYPE"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, text=f.get_type_message(query_list[ind][_ACTION]), reply_markup=k.get_type_keyboard())
    return query_list

def br_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_SECTION] = "BR"
    query_list[ind][_NEXT_STEP] = "TYPE"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.message.chat.id, text=f.get_type_message(query_list[ind][_ACTION]), reply_markup=k.get_type_keyboard())
    return query_list

def bcup_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_SECTION] = "BCup"
    query_list[ind][_NEXT_STEP] = "PART"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    mas = f.get_parts_list_from_db("BCup%", connection)
    bot.send_message(call.message.chat.id, text="Выберите деталь", 
                     reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
    return query_list

def stand_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_SECTION] = "STAND"
    query_list[ind][_NEXT_STEP] = "PART"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    mas = f.get_parts_list_from_db("%STAND%", connection)
    bot.send_message(call.message.chat.id, text="Выберите деталь", 
                     reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
    return query_list

### TYPE -> part, sb, ax, acc, body ##################################################################################################################
######################################################################################################################################################
def part_type_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_TYPE] = "part"
    query_list[ind][_NEXT_STEP] = "PART"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    mas = f.get_parts_list_from_db(query_list[ind][_SECTION] + "\_0%", connection)
    bot.send_message(call.message.chat.id, text="Выберите деталь", 
                     reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
    return query_list

def sb_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_TYPE] = "sb"
    query_list[ind][_NEXT_STEP] = "PART"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    mas = f.get_parts_list_from_db(query_list[ind][_SECTION] + "\_SB%", connection)
    bot.send_message(call.message.chat.id, text="Выберите деталь", 
                     reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
    return query_list

def ax_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_TYPE] = "ax"
    query_list[ind][_NEXT_STEP] = "PART"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    mas = f.get_parts_list_from_db(query_list[ind][_SECTION] + "(%", connection)
    bot.send_message(call.message.chat.id, text="Выберите деталь", 
                     reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
    return query_list

def num_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_TYPE] = 'num'
    query_list[ind][_NEXT_STEP] = "PART"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    mas = f.get_bodys_parts_list_from_db(connection, query_list[ind][_SECTION].lower())
    bot.send_message(call.message.chat.id, text="Выберите деталь", 
                     reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
    return query_list

def acc_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_TYPE] = "acc"
    query_list[ind][_NEXT_STEP] = "PART"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    mas = f.get_parts_list_from_db(query_list[ind][_SECTION] + "\_ACC%", connection)
    bot.send_message(call.message.chat.id, text="Выберите деталь", 
                     reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
    return query_list

def body_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_TYPE] = "body"
    query_list[ind][_NEXT_STEP] = "PART"
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    mas = f.get_parts_list_from_db("W_" + query_list[ind][_SECTION] + "%", connection)
    bot.send_message(call.message.chat.id, text="Выберите деталь", 
                     reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
    return query_list

### PART #############################################################################################################################################
######################################################################################################################################################
def part_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data != 'next':
        query_list[ind][_PART] += '|' + call.data
        if query_list[ind][_TYPE] == 'part':
            mas = f.get_parts_list_from_db(query_list[ind][_SECTION] + "\_0%", connection)
            bot.send_message(call.message.chat.id, text="Выберите деталь", 
                             reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
        elif query_list[ind][_TYPE] == 'sb':
            mas = f.get_parts_list_from_db(query_list[ind][_SECTION] + "\_SB%", connection)
            bot.send_message(call.message.chat.id, text="Выберите деталь", 
                             reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
        elif query_list[ind][_TYPE] == 'ax':
            mas = f.get_parts_list_from_db(query_list[ind][_SECTION] + "(%", connection)
            bot.send_message(call.message.chat.id, text="Выберите деталь", 
                             reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
        elif query_list[ind][_TYPE] == 'num':
            mas = f.get_bodys_parts_list_from_db(connection, query_list[ind][_SECTION].lower())
            bot.send_message(call.message.chat.id, text="Выберите деталь", 
                             reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
        elif query_list[ind][_TYPE] == 'acc':
            mas = f.get_parts_list_from_db(query_list[ind][_SECTION] + "\_ACC%", connection)
            bot.send_message(call.message.chat.id, text="Выберите деталь", 
                             reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
        elif query_list[ind][_TYPE] == 'body':
            mas = f.get_parts_list_from_db("W_" + query_list[ind][_SECTION] + "%", connection)
            bot.send_message(call.message.chat.id, text="Выберите деталь", 
                             reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
        elif query_list[ind][_SECTION] == 'BCup':
            mas = f.get_parts_list_from_db("BCup%", connection)
            bot.send_message(call.message.chat.id, text="Выберите деталь", 
                                reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
        elif query_list[ind][_SECTION] == 'STAND':
            mas = f.get_parts_list_from_db("%STAND%", connection)
            bot.send_message(call.message.chat.id, text="Выберите деталь", 
                                reply_markup=k.get_keyboard_from_array_with_next_button(mas, query_list[ind][_PART].split('|')[1:]))
    else:
        parts = query_list[ind][_PART].split('|')[1:]
        if query_list[ind][_ACTION] == 'know':
            if query_list[ind][_TYPE] == 'num':
                query_list[ind][_NEXT_STEP] = 'BODYNUM'
                mas = f.get_bodys_num_by_section(connection, query_list[ind][_SECTION])
                if len(mas) > 0:
                    bot.send_message(call.message.chat.id, text='Выберите номер тела',
                                 reply_markup=k.get_keyboard_from_array(mas))
                else:
                    bot.send_message(call.message.chat.id,
                                    text='Подходящих тел нет в работе, уточните информацию')
            else:
                f.correct_data_in_db(query_list[ind], call.message.chat.username, call, connection, bot)
        else:
            query_list[ind][_NEXT_STEP] = "STAGE"
            mas = f.get_stages_list_from_db(parts[0], connection)
            query_list[ind][_NEXT_PART] += 1
            bot.send_message(call.message.chat.id, text="Выберите состояние детали " + parts[0] + ":", 
                            reply_markup=k.get_keyboard_from_array(mas))
    return query_list

### STAGE ############################################################################################################################################
######################################################################################################################################################
def stage_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    query_list[ind][_STAGE] += '|' + call.data

    num = query_list[ind][_NEXT_PART]
    parts = query_list[ind][_PART].split('|')[1:]
    stages = query_list[ind][_STAGE].split('|')[1:]

    if num < len(parts):
        mas = f.get_stages_list_from_db(parts[num], connection)
        query_list[ind][_NEXT_PART] += 1
        bot.send_message(call.message.chat.id, text='Выберите состояние детали ' + parts[num] + ':',
                        reply_markup=k.get_keyboard_from_array(mas))
    else:
        if query_list[ind][_ACTION] == 'know':
            f.correct_data_in_db(query_list[ind], call.message.chat.username, call, connection, bot)
        elif query_list[ind][_TYPE] == 'num':
            if parts[0].find('W') == 0:
                with connection.cursor() as cursor:
                    try:
                        # Определяем мин.номер тела без нужного колена
                        cursor.execute('''SELECT serial_number 
                                       FROM instruments
                                       WHERE status='in work'
                                       ORDER BY serial_number''')
                        mas = cursor.fetchall()
                        serials = []
                        for i in range(len(mas)):
                            serials.append(mas[i][0])
                        print(serials)
                        serial = -1
                        for i in range(len(serials)):
                            cursor.execute('''SELECT count(*) 
                                           FROM bodys 
                                           WHERE serial_number=%s 
                                           AND section=%s''', 
                                           (serials[i], query_list[ind][_SECTION], ))
                            if cursor.fetchall()[0][0] == 0:
                                serial = serials[i]
                                break
                        print(serial)

                        # Если подходящего инструмента нет
                        if serial == -1:
                            # Генерируем номер инструмента
                            cursor.execute('''SELECT date_part('year', CURRENT_TIMESTAMP);''')
                            year = str(int(cursor.fetchall()[0][0]))
                            if len(serials) == 0:
                                number = 1
                            else:
                                number = str(int(serials[len(serials) - 1][3:]) + 1)
                            while len(number) < 3:
                                number = '0' + number
                            serial = 'B' + year[2:] + number

                            # Добавляем номер в instruments
                            cursor.execute('''INSERT INTO instruments
                                           (serial_number, status)
                                           VALUES (%s, 'in work')''', 
                                           (serial, ))
                            
                        # Добавляем номер с коленом в bodys
                        cursor.execute('''INSERT INTO bodys
                                       (section, serial_number, status)
                                       VALUES (%s, %s, 'in work')''', 
                                       (query_list[ind][_SECTION], serial, ))
                        
                        # Добавляем элементы колена в bodys_list
                        cursor.execute('''SELECT * FROM {table}'''
                                       .format(table=query_list[ind][_SECTION].lower() + '_list'))
                        mas = cursor.fetchall()
                        cursor.execute('''SELECT id FROM ''')
                    except Exception as _ex:
                        print("Some problem in SELECT serial_number FROM instruments...", _ex)
            else:
                query_list[ind][_NEXT_PART] = 0
                query_list[ind][_NEXT_STEP] = 'BODYNUM'
                mas = f.get_bodys_num_by_section(connection, query_list[ind][_SECTION].upper())
                if len(mas) > 0:
                    bot.send_message(call.message.chat.id, 
                                    text='Выберите номер тела, которому принадлежат детали:\n',
                                    reply_markup=k.get_keyboard_from_array(mas))
                else:
                    bot.send_message(call.message.chat.id,
                                    text='Подходящих тел нет в работе, уточните информацию')
        else:
            query_list[ind][_NEXT_PART] = 0
            query_list[ind][_NEXT_STEP] = 'COUNT'
            bot.send_message(call.message.chat.id, 
                            text='Введите количество ' 
                                + parts[0] + ', ' 
                                + stages[0] + ': ', 
                            reply_markup=k.get_numpad())

    return query_list

### COUNT ############################################################################################################################################
######################################################################################################################################################
def count_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    num = query_list[ind][_NEXT_PART]
    parts = query_list[ind][_PART].split('|')[1:]
    stages = query_list[ind][_STAGE].split('|')[1:]
    counts = query_list[ind][_COUNT].split('|')[1:]
    print(counts)
    if 48 <= ord(call.data[_ACTION]) <= 57:
        if(num >= len(counts)):
            counts.append('')
        counts[num] += call.data
        query_list[ind][_COUNT] = f.gen_count_str_from_arr(counts)
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text="Введите количество "
                                      + parts[num] + ", " 
                                      + stages[num] + ': '
                                      + counts[num])
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                        message_id=call.message.message_id,
                                        reply_markup=k.get_numpad())
            
    elif call.data == "backspace":
        if num < len(counts):
            if len(counts[num]) > 0:
                counts[num] = counts[num][:-1]
        query_list[ind][_COUNT] = f.gen_count_str_from_arr(counts)
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text="Введите количество "
                                      + parts[num] + ", " 
                                      + stages[num] + ': '
                                      + counts[num])
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                        message_id=call.message.message_id,
                                        reply_markup=k.get_numpad())
        except:
            pass
    
    elif call.data == "enter":
        if num < len(parts) - 1:
            query_list[ind][_NEXT_PART] += 1
            num = query_list[ind][_NEXT_PART]
            parts = query_list[ind][_PART].split('|')[1:]
            stages = query_list[ind][_STAGE].split('|')[1:]
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                    message_id=call.message.message_id, 
                                    text="Введите количество "
                                      + parts[num] + ", " 
                                      + stages[num] + ': ')
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                            message_id=call.message.message_id,
                                            reply_markup=k.get_numpad())
        else:
            query_list[ind][_NEXT_STEP] = "APPROVE"
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            t = f.get_approve_text(query_list[ind])
            bot.send_message(call.message.chat.id, text="Вы выбрали: " + t, reply_markup=k.get_approve_keyboard())
    return query_list

### BODYNUM ##########################################################################################################################################
######################################################################################################################################################
def bodynum_handler(query_list, call, bot, connection):
    ind = users_list.index(call.message.chat.username)
    query_list[ind][_BODYNUM] = call.data
    if query_list[ind][_ACTION] == 'know':
        f.correct_data_in_db(query_list[ind], call.message.chat.username, call, connection, bot)
    else:
        query_list[ind][_NEXT_STEP] = 'APPROVE'
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        t = f.get_approve_text(query_list[ind])
        bot.send_message(call.message.chat.id, text="Вы выбрали: " + t, reply_markup=k.get_approve_keyboard())
    return query_list

### APPROVE ##########################################################################################################################################
######################################################################################################################################################
def approve_handler(query_list, call, bot, connection):
    if call.data == "yes":
        ind = users_list.index(call.message.chat.username)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        f.correct_data_in_db(query_list[ind], call.message.chat.username, call, connection, bot)
        query_list[ind] = ["", "", "", "", "", "", "", "", 0]

    elif call.data == "no":
        ind = users_list.index(call.message.chat.username)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, text="Отмена")
        query_list[ind] = ["", "", "", "", "", "", "", "", 0]
    return query_list