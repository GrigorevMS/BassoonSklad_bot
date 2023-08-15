import telebot
import psycopg2
import os
import socket
import time
from const import users_list, body_num_stages, _ACTION, _SECTION, _TYPE, _PART, _STAGE, _COUNT, _BODYNUM, _NEXT_STEP, _NEXT_PART
import functions as f
import keyboards as k
import message_handler as h

# Объявление бота, списка пользователей и очереди команд пользователей
bot = telebot.TeleBot("5864465325:AAFR4WaB217ndS5YQR3dEXZCRkU4PSeveW8")

# Подключение к базе данных
connection = f.getConnection()

# Команда одного полльзователя - действие, деталь, состояние, количество
query_list = [["", "", "", "", "", "", "", "", 0] for i in range(len(users_list))]

# Чтение файла текста ответа команды help
fin = open("bot_help.txt", mode="r", encoding="utf-8")
bot_help_list = fin.readlines()
fin.close()
bot_help_text = ""
for line in bot_help_list:
    bot_help_text += line

def copy_query(arr):
    out = [["", "", "", "", "", "", ""] for i in range(len(users_list))]
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            out[i][j] = arr[i][j]
    return out

######################################################################################################################################################
######################################################################################################################################################
# Обработка сообщений пользователя
@bot.message_handler(content_types=['text'])
def get_start(message):
    global query_list
    if f.check_access(message.from_user.username):
        if message.text == "/start":
            query_list = h.start_handler(query_list, message, bot, connection)
        elif message.text == "/help":
            query_list = h.help_handler(query_list, message, bot, connection, bot_help_text)
        elif message.text == "/finish":
            query_list = h.finish_handler(query_list, message, bot, connection)
    else:
        bot.send_message(message.from_user.id, "Извините, у вас нет доступа((")

@bot.callback_query_handler(func=lambda call: True)
def activity_callback_worker(call):
    global query_list
    user_ind = users_list.index(call.message.chat.username)
    ######################################################################################################################################################
    # Обработка клавиатуры выбора действия
    if query_list[user_ind][_NEXT_STEP] == "ACTION":
        if call.data == "get":
            query_list = h.get_handler(query_list, call, bot, connection)
        elif call.data == "put":
            query_list = h.put_handler(query_list, call, bot, connection)
        elif call.data == "know":
            query_list = h.know_handler(query_list, call, bot, connection)
        elif call.data == "correct":
            query_list = h.correct_handler(query_list, call, bot, connection)
        elif call.data == "getlist":
            query_list = h.getlist_handler(query_list, call, bot, connection)
        elif call.data == "getlog":
            query_list = h.getlog_handler(query_list, call, bot, connection)

    ######################################################################################################################################################
    # Обработка клавиатуры выбора группы
    elif query_list[user_ind][_NEXT_STEP] == "SECTION":
        if call.data == "BF":
            query_list = h.bf_handler(query_list, call, bot, connection)
        elif call.data == "BS":
            query_list = h.bs_handler(query_list, call, bot, connection)
        elif call.data == "BB":
            query_list = h.bb_handler(query_list, call, bot, connection)
        elif call.data == "BR":
            query_list = h.br_handler(query_list, call, bot, connection)
        elif call.data == "BCup":
            query_list = h.bcup_handler(query_list, call, bot, connection)
        elif call.data == "STAND":
            query_list = h.stand_handler(query_list, call, bot, connection)

    ######################################################################################################################################################
    # Обработка клавиатуры выбора типа
    elif query_list[user_ind][_NEXT_STEP] == "TYPE":
        if call.data == "part":
            query_list = h.part_type_handler(query_list, call, bot, connection)
        elif call.data == "sb":
            query_list = h.sb_handler(query_list, call, bot, connection)
        elif call.data == "ax":
            query_list = h.ax_handler(query_list, call, bot, connection)
        elif call.data == 'num':
            query_list = h.num_handler(query_list, call, bot, connection)
        elif call.data == "acc":
            query_list = h.acc_handler(query_list, call, bot, connection)
        elif call.data == "body":
            query_list = h.body_handler(query_list, call, bot, connection)

    ######################################################################################################################################################
    # Обработка выбора детали
    elif query_list[user_ind][_NEXT_STEP] == "PART":
        query_list = h.part_handler(query_list, call, bot, connection)

    ######################################################################################################################################################
    # Обработка клавиатуры выбора состояния
    elif query_list[user_ind][_NEXT_STEP] == "STAGE":
        query_list = h.stage_handler(query_list, call, bot, connection)
    ######################################################################################################################################################
    # Обработка клавиатуры выбора количества
    elif query_list[user_ind][_NEXT_STEP] == "COUNT":
        query_list = h.count_handler(query_list, call, bot, connection)

    # Обработка выбора номера колена
    elif query_list[user_ind][_NEXT_STEP] == 'BODYNUM':
        query_list = h.bodynum_handler(query_list, call, bot, connection)

    ######################################################################################################################################################
    # Обработка клавиатуры подтверждения
    elif query_list[user_ind][_NEXT_STEP] == "APPROVE":
        query_list = h.approve_handler(query_list, call, bot, connection)

    print(query_list)
    f.write_query_log(str(query_list), connection)

######################################################################################################################################################
######################################################################################################################################################    
while True:
    print()
    print("BassoonSklad_bot is running on " + socket.gethostname() + ". . .")
    f.write_query_log("BassoonSklad_bot is running on " + socket.gethostname() + ". . .", connection)
    print()
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as _ex:
        print("[ERROR]", _ex)
        f.write_query_log("[ERROR] " + str(_ex), connection)
