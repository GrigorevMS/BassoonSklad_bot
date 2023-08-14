import telebot
import functions as f

######################################################################################################################################################
######################################################################################################################################################
# Генерация клавиатуры выбора действия
def get_activity_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_get = telebot.types.InlineKeyboardButton(text="Взять детали", callback_data="get")
    keyboard.add(key_get)
    key_put = telebot.types.InlineKeyboardButton(text="Положить детали", callback_data="put")
    keyboard.add(key_put)
    key_know = telebot.types.InlineKeyboardButton(text="Узнать количество", callback_data="know")
    keyboard.add(key_know)
    key_correct = telebot.types.InlineKeyboardButton(text="Скорректировать количество", callback_data="correct")
    keyboard.add(key_correct)
    key_getlist = telebot.types.InlineKeyboardButton(text="Получить ведомость", callback_data="getlist")
    keyboard.add(key_getlist)
    key_getquery = telebot.types.InlineKeyboardButton(text="Получить логи", callback_data="getlog")
    keyboard.add(key_getquery)
    return keyboard

# Генерация клавиатуры выбора группы деталей
def get_section_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_bf = telebot.types.InlineKeyboardButton(text="BF", callback_data="BF")
    keyboard.add(key_bf)
    key_bs = telebot.types.InlineKeyboardButton(text="BS", callback_data="BS")
    keyboard.add(key_bs)
    key_bb = telebot.types.InlineKeyboardButton(text="BB", callback_data="BB")
    keyboard.add(key_bb)
    key_br = telebot.types.InlineKeyboardButton(text="BR", callback_data="BR")
    keyboard.add(key_br)
    key_cup = telebot.types.InlineKeyboardButton(text="BCup", callback_data="BCup")
    keyboard.add(key_cup)
    key_stand = telebot.types.InlineKeyboardButton(text="STAND", callback_data="STAND")
    keyboard.add(key_stand)
    return keyboard

# Генерация клавиатуры выбора типа детали
def get_type_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_part = telebot.types.InlineKeyboardButton(text="Детали", callback_data="part")
    keyboard.add(key_part)
    key_sb = telebot.types.InlineKeyboardButton(text="Малые сборочные узлы", callback_data="sb")
    keyboard.add(key_sb)
    key_ax = telebot.types.InlineKeyboardButton(text="Узлы на оси", callback_data="ax")
    keyboard.add(key_ax)
    key_acc = telebot.types.InlineKeyboardButton(text="Аксессуары", callback_data="acc")
    keyboard.add(key_acc)
    #key_body = telebot.types.InlineKeyboardButton(text="Тела", callback_data="body")
    #skeyboard.add(key_body)
    return keyboard

# Генерация клавиатуры выбора детали
def get_keyboard_from_array(mas):
    keyboard = telebot.types.InlineKeyboardMarkup()
    pos = 0
    for i in range(len(mas)):
        keyboard.add(telebot.types.InlineKeyboardButton(text=mas[i][0], callback_data=mas[i][0]))
    return keyboard

# Генерация клавиатуры выбора детали для множественного выбора с подтверждением
def get_keyboard_from_array_with_next_button(mas, except_arr):
    keyboard = telebot.types.InlineKeyboardMarkup()
    pos = 0
    for i in range(len(mas)):
        if not f.chek_is_element_in_arr(except_arr, mas[i][0]):
            keyboard.add(telebot.types.InlineKeyboardButton(text=mas[i][0], callback_data=mas[i][0]))
    keyboard.add(telebot.types.InlineKeyboardButton(text='>> ДАЛЕЕ >>', callback_data='next'))
    return keyboard

# Генерация клавиатуры выбора количества
def get_numpad():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="1", callback_data="1"),
                 telebot.types.InlineKeyboardButton(text="2", callback_data="2"),
                 telebot.types.InlineKeyboardButton(text="3", callback_data="3"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="4", callback_data="4"),
                 telebot.types.InlineKeyboardButton(text="5", callback_data="5"),
                 telebot.types.InlineKeyboardButton(text="6", callback_data="6"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="7", callback_data="7"),
                 telebot.types.InlineKeyboardButton(text="8", callback_data="8"),
                 telebot.types.InlineKeyboardButton(text="9", callback_data="9"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="<<<", callback_data="backspace"),
                 telebot.types.InlineKeyboardButton(text="0", callback_data="0"),
                 telebot.types.InlineKeyboardButton(text="enter", callback_data="enter"))
    return keyboard

# Генерация клавиатуры подтверждения
def get_approve_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Да", callback_data="yes"),
                 telebot.types.InlineKeyboardButton(text="Нет", callback_data="no"))
    return keyboard