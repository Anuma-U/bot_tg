import sqlite3


connection = sqlite3.connect("./database/products_database.db")
cursor = connection.cursor()



def initiate_db():
    connection = sqlite3.connect("./database/products_database.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')

# cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)", ("Помаргалдын", "Чтобы сердце не тудым тудым", "1596"))
# cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)", ("Пурген", "Для приятного время припровождения", "18953"))
# cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)", ("Глицин", "Универсальное лекарство от всех болезней в школе", "162"))
# cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)", ("Активированный уголь", "Чтобы его активировать скажите 3 цифры на обороте карты", "1675"))


def get_all_products(id):
    initiate_db()
    connection = sqlite3.connect("./database/products_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT title, description, price FROM Products WHERE id = ?", (id,))
    return cursor.fetchone()


connection.commit()
connection.close()