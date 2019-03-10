# Some text
import xlrd
import sqlite3
dbname = 'movies.db'
xlsname = 'movies.xlsx'  #movies.xlsx
global cur
global conn

def pasre_excel_to_sqlite(xlsname=xlsname, dbname=dbname):   # strings

    def copy_A_from_B(list1, list2):
        result = True
        while result:
            list_return = [x for x in list1 for y in list2 if x==y]
            result = not any(elem in list1 for elem in list2)
        return list_return

    def capitalize_items_in_list(list1):
        for item in list1:
            list1[list1.index(item)] = item.capitalize()
        return list1

    def sublist_to_string(mainlist):
        for sublist in mainlist:
            mainlist[mainlist.index(sublist)] = ', '.join(sublist)
        return mainlist

    print('Parsing Excel File...')
    workbook = xlrd.open_workbook(xlsname)
    sheet = workbook.sheet_by_index(0)
    data = [sheet.cell_value(row,column) for column in range(sheet.ncols) for row in range(sheet.nrows)]

    countrylist = ['Дания', 'Венгрия', 'Нидерланды', 'Австралия', 'Швеция', 'Китай', 'Италия', 'Германия', 'Франция', 'Великобритания', 'Россия', 'Гонконг', 'Колумбия', 'Испания', 'Бельгия', 'Норвегия', 'Канада', 'Сша', 'Япония']
    genrelist = ['Экранизация', 'Мюзикл', 'Вестерн', 'Триллер', 'Криминал', 'Боевик', 'Драма', 'Мелодрама', 'Детектив', 'Семейный', 'Музыка', 'Ужасы', 'История', 'Биография', 'Военный', 'Комедия', 'Фантастика', 'Фэнтези', 'Приключения']

    # ['Яркость / Bright', '(Дэвид Эйр / David Ayer)', '[2017, США, Фантастика, фэнтези, боевик, триллер, криминал, WEBRip]', 'MVO', '(NewStudio)', '+ Original', '(Eng)', '+ Sub', '(Rus, Eng)']
    #     title                 director                year   country                      genre                   ripinfo
    infolist = [line.split('\xa0') for line in data]
    title = [x[0] for x in infolist]
    director = [x[1][1:-2] for x in infolist]
    misc_info = [x[2][1:-2].split(', ') for x in infolist]
    misc_info = [capitalize_items_in_list(x) for x in misc_info]
    year = [int(item.pop(0)) for item in misc_info]
    ripinfo = [item.pop(-1) for item in misc_info]
    country = [copy_A_from_B(movie,countrylist) for movie in misc_info]  # вытягивает совпадения
    country = sublist_to_string(country) # ['Великобритания', 'Китай', 'Сша']  >>>  ['Великобритания, Китай, Сша']
    genre = [copy_A_from_B(movie,genrelist) for movie in misc_info] # вытягивает совпадения
    genre = sublist_to_string(genre) # ['Великобритания', 'Китай', 'Сша']  >>>  ['Великобритания, Китай, Сша']
    main_table = [item for item in zip(title,year,director,country,genre)]
    print('{} items aquired'.format(len(main_table)))

    print('Creating Database...')
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS movies')
    cur.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, year INTEGER, director TEXT, country TEXT, genre TEXT)")
    cur.executemany("INSERT INTO movies(title,year,director,country,genre) VALUES(?,?,?,?,?)",(main_table))
    conn.commit()
    conn.close()
    print('Database Created')

def connect():
    conn=sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, year INTEGER, director TEXT, country TEXT, genre TEXT)")
    conn.commit()
    conn.close()
    print('Connected to {} database.'.format(dbname))

def search(title=None, genre=None, director=None, country=None, year=None):
    rows = []
    # DECORATOR
    def get_row_like(item,idx):
        searchlist_strings = ['title','genre','director','country','year']
        conn=sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute("SELECT * FROM movies WHERE {} LIKE ?".format(searchlist_strings[idx]), ('%'+item+'%',))
        result = set(cur.fetchall())
        conn.close()
        # print(result)
        return result

    searchlist = [title,genre,director,country,year]
    for item in searchlist:
        if item is not None:
            # print(searchlist.index(item))
            i = searchlist.index(item)
            rows.append(get_row_like(item,i))
            # print(item)

    def intersect(rows):
        if len(rows)==0:
            return []
        if len(rows)==1:
            return rows[0]  # list(set(tuple))
        if len(rows)>=2:
            args = rows[1:]
            return list(set(rows[0].intersection(*args)))

    intersect_rows = intersect(rows)
    # print(intersect_rows)
    intersect_rows = sorted(intersect_rows, key=lambda x: (x[2],x[1]))
    # print(intersect_rows)
    return intersect_rows

def view_all():
    conn=sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies")
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    rows = sorted(rows, key=lambda x: (x[2],x[1]))
    return rows
    print('All rows selected to view')

def insert_row(title,genre,director,country,year):
    conn=sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("INSERT INTO movies VALUES (NULL,?,?,?,?,?)",(title,genre,director,country,year))
    conn.commit()
    conn.close()
    print('Values inserted')

def delete_row(id):
    conn=sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("DELETE FROM movies WHERE id=?", (id,))
    conn.commit()
    conn.close()
    print('Row ID {} deleted'.format(id))

def update_row(id,title,genre,director,country,year):
    conn=sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("UPDATE movies SET title=?, genre=?, director=?, country=?, year=? WHERE id=?", (title,genre,director,country,year,id))
    conn.commit()
    conn.close()
    print('Row ID {} updated'.format(id))

try:
    pasre_excel_to_sqlite(xlsname,dbname)
except:
    print('Excel file not read')

connect()
