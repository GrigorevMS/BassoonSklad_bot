import xlrd
import xlwt
import psycopg2

def head_body_style(pattern=None):

    style = xlwt.XFStyle()  # Create Style

    # Установить стиль шрифта
    font = xlwt.Font()  # Create Font
    font.name = "Century Gothic"  # Песня Ti
    font.height = 20 * 11  # размер шрифта

    # Установить стиль ячейки
    style.alignment.vert = style.alignment.VERT_CENTER
    style.alignment.horz = style.alignment.HORZ_CENTER
    style.alignment.wrap = style.alignment.WRAP_AT_RIGHT

    # Установить фон ячейки
    if pattern:
        pattern = xlwt.Pattern()  # Create Pattern
        pattern.pattern = pattern.SOLID_PATTERN  # Установить цвет фона
        pattern.pattern_fore_colour = 22  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        pattern.pattern_back_colour = 6
        style.pattern = pattern

    # Установить стиль границы
    borders = xlwt.Borders()  # Pattern Borders

    borders.right = borders.MEDIUM
    borders.top = borders.MEDIUM
    borders.bottom = borders.MEDIUM
    borders.left = borders.MEDIUM

    borders.left_colour = 0x0  # Раскраска границы
    borders.right_colour = 0x0
    borders.top_colour = 0x0
    borders.bottom_colour = 0x0

    style.font = font  # Назначение стиля
    style.borders = borders
    return style

def cell_body_style(pattern=None):

    style = xlwt.XFStyle()  # Create Style

    # Установить стиль шрифта
    font = xlwt.Font()  # Create Font
    font.name = "Century Gothic"  # Песня Ti
    font.height = 20 * 11  # размер шрифта

    # Установить стиль ячейки
    style.alignment.vert = style.alignment.VERT_CENTER
    style.alignment.horz = style.alignment.HORZ_CENTER
    style.alignment.wrap = style.alignment.WRAP_AT_RIGHT

    # Установить фон ячейки
    if pattern:
        pattern = xlwt.Pattern()  # Create Pattern
        pattern.pattern = pattern.SOLID_PATTERN  # Установить цвет фона
        pattern.pattern_fore_colour = 22  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        pattern.pattern_back_colour = 6
        style.pattern = pattern

    # Установить стиль границы
    borders = xlwt.Borders()  # Pattern Borders

    borders.right = borders.MEDIUM
    #borders.top = borders.THIN
    #borders.bottom = borders.THIN
    borders.left = borders.MEDIUM

    borders.left_colour = 0x0  # Раскраска границы
    borders.right_colour = 0x0
    borders.top_colour = 0x0
    borders.bottom_colour = 0x0

    style.font = font  # Назначение стиля
    style.borders = borders
    return style

def border_cell_body_style(pattern=None):

    style = xlwt.XFStyle()  # Create Style

    # Установить стиль шрифта
    font = xlwt.Font()  # Create Font
    font.name = "Century Gothic"  # Песня Ti
    font.height = 20 * 11  # размер шрифта

    # Установить стиль ячейки
    style.alignment.vert = style.alignment.VERT_CENTER
    style.alignment.horz = style.alignment.HORZ_CENTER
    style.alignment.wrap = style.alignment.WRAP_AT_RIGHT

    # Установить фон ячейки
    if pattern:
        pattern = xlwt.Pattern()  # Create Pattern
        pattern.pattern = pattern.SOLID_PATTERN  # Установить цвет фона
        pattern.pattern_fore_colour = 22  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        pattern.pattern_back_colour = 6
        style.pattern = pattern

    # Установить стиль границы
    borders = xlwt.Borders()  # Pattern Borders

    borders.right = borders.MEDIUM
    #borders.top = borders.THIN
    borders.bottom = borders.MEDIUM
    borders.left = borders.MEDIUM

    borders.left_colour = 0x0  # Раскраска границы
    borders.right_colour = 0x0
    borders.top_colour = 0x0
    borders.bottom_colour = 0x0

    style.font = font  # Назначение стиля
    style.borders = borders
    return style

def get_data(connection, pattern):
    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT
                                parts.id,
                                parts.name,
                                stages.name,
                                stages.count
                              FROM parts 
                              JOIN stages 
                                ON parts.id = stages.part_id
                              WHERE parts.id 
                                LIKE %s
                              ORDER BY parts.id""", (pattern, ))
            return cursor.fetchall()
        except:
            pass

def sort_stage_arr(arr):
    temp = []
    way = ["оттокаренные",
           "восковые",
           "в блоках",
           "отделенные",
           "опиленные",
           "паянные",
           "шлифованные",
           "полированные",
           "галтовка",
           "гальваника",
           "серебро",
           "никель",
           "нарезанные",
           "с резьбой",
           "со шлицем"]
    for j in range(len(way)):
        for q in range(len(arr)):
            if arr[q][2] == way[j]:
                temp.append(arr[q])
    return temp
        

def split_data(data):
    ind_arr = [0]
    for i in range(1, len(data)):
        if data[i][0] != data[i - 1][0]:
            ind_arr.append(i)
    ind_arr.append(len(data))
    temp = []
    for i in range(1, len(ind_arr)):
        temp.append(data[ind_arr[i - 1]: ind_arr[i]])

    for i in range(len(temp)):
        temp[i] = sort_stage_arr(temp[i])
    return temp

def clear_data(data):
    for i in range(len(data)):
        for j in range(1, len(data[i])):
            temp = ["", ""]
            temp.append(data[i][j][2])
            temp.append(data[i][j][3])

            data[i][j] = temp
    return data

def gen_sheet(sheet, data, cell_style, border_cell_style):
    data = split_data(data)
    data = clear_data(data)
    line = 1
    for i in range(len(data)):
        for j in range(len(data[i])):
            if j < len(data[i]) - 1:
                sheet.write(line, 0, data[i][j][0], cell_style)
                sheet.write(line, 1, data[i][j][1], cell_style)
                sheet.write(line, 2, data[i][j][2], cell_style)
                sheet.write(line, 3, data[i][j][3], cell_style)
            else:
                sheet.write(line, 0, data[i][j][0], border_cell_style)
                sheet.write(line, 1, data[i][j][1], border_cell_style)
                sheet.write(line, 2, data[i][j][2], border_cell_style)
                sheet.write(line, 3, data[i][j][3], border_cell_style)
            line += 1
        
# Подключение к БД
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
    print("[INFO] Successfully connected to PostgreSQL . . .")
except Exception as _ex:
    print("[INFO] Some problem with connecting to PostgreSQL . . .")

book = xlwt.Workbook(encoding = 'utf-8')

book.add_sheet("BF")
book.add_sheet("BS")
book.add_sheet("BB")
book.add_sheet("BR")
book.add_sheet("BCup")
book.add_sheet("BF_ACC")
book.add_sheet("BS_ACC")
book.add_sheet("BB_ACC")
book.add_sheet("BR_ACC")

head_style = head_body_style(True)
cell_style = cell_body_style()
border_cell_style = border_cell_body_style()

for i in range(9):
    sheet = book.get_sheet(i)
    for c in range(4):
        sheet.col(c).width = 256 * 30
    sheet.row(0).height_mismatch = True
    sheet.row(0).height = 500
    sheet.write(0, 0, "ОБОЗНАЧЕНИЕ", head_style)
    sheet.write(0, 1, "НАИМЕНОВАНИЕ", head_style)
    sheet.write(0, 2, "ЭТАП", head_style)
    sheet.write(0, 3, "КОЛИЧЕСТВО", head_style)

# BF
gen_sheet(book.get_sheet(0), get_data(connection, "BF\_0%") + get_data(connection, "BF\_SB%") + get_data(connection, "BF(%"), cell_style, border_cell_style)
# BS
gen_sheet(book.get_sheet(1), get_data(connection, "BS\_0%") + get_data(connection, "BS\_SB%") + get_data(connection, "BS(%"), cell_style, border_cell_style)
# BB
gen_sheet(book.get_sheet(2), get_data(connection, "BB\_0%") + get_data(connection, "BB\_SB%") + get_data(connection, "BB(%"), cell_style, border_cell_style)
# BR
gen_sheet(book.get_sheet(3), get_data(connection, "BR\_0%") + get_data(connection, "BR\_SB%") + get_data(connection, "BR(%"), cell_style, border_cell_style)
# BCup
gen_sheet(book.get_sheet(4), get_data(connection, "BCup\_%"), cell_style, border_cell_style)
# BF_ACC
gen_sheet(book.get_sheet(5), get_data(connection, "BF\_ACC%"), cell_style, border_cell_style)
# BS_ACC
gen_sheet(book.get_sheet(6), get_data(connection, "BF\_ACC%"), cell_style, border_cell_style)
# BB_ACC
gen_sheet(book.get_sheet(7), get_data(connection, "BF\_ACC%"), cell_style, border_cell_style)
# BR_ACC
gen_sheet(book.get_sheet(8), get_data(connection, "BF\_ACC%"), cell_style, border_cell_style)

book.save("BassoonPartsList.xls")

connection.close()
