import sqlite3

connection = sqlite3.connect('database.db')
connection2 = sqlite3.connect('login.db')

with open ('schema.sql') as f:
    connection2.executescript(f.read())

cursor = connection.cursor()
cursor2 = connection2.cursor()


def add_text(text_value):
    cursor.execute("INSERT INTO mytable(ID,text_value) VALUES (DEFAULT, %s)",(text_value))
    connection.commit()
    return 1

connection2.commit()
connection2.close()
connection.close()
