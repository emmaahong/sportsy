import sqlite3

connection = sqlite3.connect('database.db')

# with open ('schema.sql') as f:
#     connection.executescript(f.read())

cursor = connection.cursor()

def add_text(text_value):
    cursor.execute("INSERT INTO mytable(ID,text_value) VALUES (DEFAULT, %s)",(text_value))
    connection.commit()
    return 1

cursor.execute(
    "INSERT INTO users (username, passcode) VALUES (?, ?)",
    ('Emma','Hello')
)

connection.commit()
connection.close()