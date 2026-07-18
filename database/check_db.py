import sqlite3

conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(assignments)")

for column in cursor.fetchall():
    print(column)

conn.close()
