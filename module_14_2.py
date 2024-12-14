import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id integer primary key,
username text not null,
email text not null,
age integer,
balance integer not null)
''')

# for i in range(1, 11):
#     cursor.execute("insert into Users(username, email, age, balance) values(?, ?, ?, ?)", (f"User{i}", f"example{i}@gmail.com", f"{i}0", "1000"))
# for i in range(1, 11, 2):
#     cursor.execute("update Users set balance = ? where username = ?", ("500", f"User{i}"))
# for i in range(1, 11, 3):
#     cursor.execute("delete from Users where username = ?", (f"User{i}", ))

cursor.execute("select username, email, age, balance from Users")
users = cursor.fetchall()
for user in users:
    print(f"Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[-1]}")

cursor.execute("delete from Users where id = ?", (6, ))
cursor.execute("select count(*) from Users")
cnt_lines = cursor.fetchone()[0]
cursor.execute("select sum(balance) from Users")
sum_balance = cursor.fetchone()[0]
cursor.execute("select avg(balance) from Users")
print(cursor.fetchone()[0])
print(sum_balance/cnt_lines)


connection.commit()
connection.close()