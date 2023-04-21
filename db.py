import sqlite3
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
def add_text(text_value):
    cursor.execute("INSERT INTO mytable(ID,text_value) VALUES (DEFAULT, %s)",(text_value))
    connection.commit()
    return 1

