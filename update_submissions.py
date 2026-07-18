import sqlite3

conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE submissions
    ADD COLUMN file_name TEXT
    """)
    print("✅ file_name added.")
except Exception as e:
    print(e)

try:
    cursor.execute("""
    ALTER TABLE submissions
    ADD COLUMN file_path TEXT
    """)
    print("✅ file_path added.")
except Exception as e:
    print(e)

conn.commit()
conn.close()

print("🎉 Submissions table updated successfully!")
