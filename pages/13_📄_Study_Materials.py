import streamlit as st
import sqlite3
import os

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favocon.png",
    layout="wide"
)

st.title("📚 Study Materials")

# -----------------------------
# Login Check
# -----------------------------
student_email = st.session_state.get("student_email")

if not student_email:
    st.error("Please login first.")
    st.stop()

# -----------------------------
# Database
# -----------------------------
conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

# Find connected teacher
cursor.execute("""
SELECT teacher_id
FROM student_teacher
WHERE student_email=?
""", (student_email,))

teacher = cursor.fetchone()

if teacher is None:
    st.warning("You are not connected to any teacher.")
    conn.close()
    st.stop()

teacher_id = teacher[0]

# Get all materials
cursor.execute("""
SELECT
file_name
FROM materials
WHERE teacher_id=?
ORDER BY id DESC
""", (teacher_id,))

materials = cursor.fetchall()

conn.close()

# -----------------------------
# Display Materials
# -----------------------------
if len(materials) == 0:

    st.info("No study materials uploaded yet.")

else:

    for material in materials:

        file_name = material[0]

        file_path = os.path.join(
            "uploads",
            "materials",
            file_name
        )

        st.subheader(f"📄 {file_name}")

        if os.path.exists(file_path):

            with open(file_path, "rb") as pdf:

                st.download_button(
                    "⬇ Download PDF",
                    pdf,
                    file_name=file_name,
                    mime="application/pdf",
                    key=file_name
                )

        else:

            st.warning("File not found.")

        st.divider()
