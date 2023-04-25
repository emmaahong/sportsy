import sqlite3

connection = sqlite3.connect('database.db')

with open ('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO users (username, passcode) VALUES (?, ?)",
    ('Emma','Hello')
)

connection.commit()
connection.close()