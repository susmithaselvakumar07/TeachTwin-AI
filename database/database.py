import sqlite3

# Create or connect to database
conn = sqlite3.connect("teachtwin.db")

# Cursor
cursor = conn.cursor()

# Teacher Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    department TEXT NOT NULL,
    subject TEXT NOT NULL,
    teachtwin_id TEXT UNIQUE,
    college TEXT NOT NULL


)
""")

# Student - Teacher Connection Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_teacher(

id INTEGER PRIMARY KEY AUTOINCREMENT,

student_email TEXT,

teacher_id TEXT

)
""")
# Student Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    department TEXT NOT NULL,
    college TEXT NOT NULL
)
""")

# Uploaded Materials Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS materials(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    teacher_id TEXT NOT NULL,

    file_name TEXT NOT NULL,

    extracted_text TEXT NOT NULL

)
""")

# -----------------------------
# Assignments Table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    teacher_id TEXT NOT NULL,

    title TEXT NOT NULL,

    description TEXT NOT NULL,

    due_date TEXT NOT NULL,

    question_file_name TEXT,

    question_file_path TEXT,

    created_on TEXT NOT NULL

)
""")

conn.commit()

# -----------------------------
# Assignment Submissions
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS submissions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    assignment_id INTEGER NOT NULL,

    student_email TEXT NOT NULL,

    student_name TEXT NOT NULL,

    file_name TEXT NOT NULL,

    file_path TEXT NOT NULL,

    submitted_on TEXT NOT NULL

)
""")
conn.commit()
conn.close()
print("Database Created Successfully ✅")
