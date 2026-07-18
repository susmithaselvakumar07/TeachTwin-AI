import sqlite3

conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE assignments
    ADD COLUMN question_file_name TEXT
    """)
    print("✅ question_file_name added.")
except Exception as e:
    print(e)

try:
    cursor.execute("""
    ALTER TABLE assignments
    ADD COLUMN question_file_path TEXT
    """)
    print("✅ question_file_path added.")
except Exception as e:
    print(e)

conn.commit()
conn.close()

print("🎉 Database Updated Successfully!")
