import sqlite3

DB_NAME = "teachtwin.db"

def generate_teachtwin_id(department):
    """
    Generate TeachTwin ID
    Example:
    TT-CSE-001
    TT-AIDS-002
    TT-IT-003
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Get total number of teachers
    cursor.execute("SELECT COUNT(*) FROM teachers")
    count = cursor.fetchone()[0] + 1

    conn.close()

    department = department.strip().upper()

    return f"TT-{department}-{count:03d}"
