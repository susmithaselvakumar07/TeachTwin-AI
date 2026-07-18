import streamlit as st
import sqlite3
import os
from datetime import datetime

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="wide"
)

st.title("📝 Assignments")

# -----------------------------
# Login Check
# -----------------------------
student_email = st.session_state.get("student_email")
student_name = st.session_state.get("student_name")

if not student_email:
    st.error("Please login first.")
    st.stop()

# -----------------------------
# Database
# -----------------------------
conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

# -----------------------------
# Find Connected Teacher
# -----------------------------
cursor.execute("""
SELECT teacher_id
FROM student_teacher
WHERE student_email=?
""", (student_email,))

teacher = cursor.fetchone()

if teacher is None:
    conn.close()
    st.warning("You are not connected to any teacher.")
    st.stop()

teacher_id = teacher[0]

# -----------------------------
# Get Assignments
# -----------------------------
cursor.execute("""
SELECT
id,
title,
description,
due_date,
question_file_name,
question_file_path
FROM assignments
WHERE teacher_id=?
ORDER BY id DESC
""", (teacher_id,))

assignments = cursor.fetchall()

if len(assignments) == 0:
    conn.close()
    st.info("No assignments available.")
    st.stop()

# -----------------------------
# Display Assignments
# -----------------------------
for assignment in assignments:

    assignment_id = assignment[0]

    st.subheader(f"📌 {assignment[1]}")

    st.write("### 📖 Description")
    st.write(assignment[2])

    st.write(f"📅 **Due Date:** {assignment[3]}")

# -----------------------------
# Download Assignment Question
# -----------------------------
question_file_name = assignment[4]
question_file_path = assignment[5]

if question_file_path is None or question_file_path == "":
    st.info("ℹ️ This assignment was created before PDF upload support.")
else:
    if os.path.exists(question_file_path):

        with open(question_file_path, "rb") as pdf:

            st.download_button(
                "📄 Download Assignment Question",
                pdf,
                file_name=question_file_name,
                mime="application/pdf",
                key=f"download_{assignment_id}"
            )

    else:
        st.warning("⚠️ Assignment PDF not found.")
    st.write("---")

    uploaded_file = st.file_uploader(
        "📤 Upload Your Assignment (PDF / DOCX)",
        type=["pdf", "docx"],
        key=f"upload_{assignment_id}"
    )

    if st.button("✅ Submit Assignment", key=f"submit_{assignment_id}"):

        if uploaded_file is None:

            st.warning("Please upload your assignment before submitting.")

        else:

            os.makedirs("uploads/submissions", exist_ok=True)

            file_path = os.path.join(
                "uploads/submissions",
                uploaded_file.name
            )

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            cursor.execute("""
            INSERT INTO submissions
            (
                assignment_id,
                student_email,
                student_name,
                file_name,
                file_path,
                submitted_on
            )
            VALUES(?,?,?,?,?,?)
            """, (

                assignment_id,
                student_email,
                student_name,
                uploaded_file.name,
                file_path,
                str(datetime.now())

            ))

            conn.commit()

            st.success("🎉 Assignment Submitted Successfully!")

    st.divider()

conn.close()
