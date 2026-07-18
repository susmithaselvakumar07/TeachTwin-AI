import streamlit as st
import sqlite3
import os
from datetime import datetime

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="centered"
)

st.title("📝 Create Assignment")

# -----------------------------
# Login Check
# -----------------------------
teacher_id = st.session_state.get("teacher_id")

if not teacher_id:
    st.error("Please login first.")
    st.stop()

# -----------------------------
# Assignment Details
# -----------------------------
title = st.text_input("📌 Assignment Title")

description = st.text_area("📝 Assignment Description")

due_date = st.date_input("📅 Due Date")

uploaded_pdf = st.file_uploader(
    "📄 Upload Assignment Question (PDF)",
    type=["pdf"]
)

# -----------------------------
# Publish Button
# -----------------------------
if st.button("🚀 Publish Assignment", use_container_width=True):

    if title == "" or description == "":
        st.warning("Please fill all fields.")

    elif uploaded_pdf is None:
        st.warning("Please upload the Assignment Question PDF.")

    else:

        # Create folder
        os.makedirs("uploads/assignments", exist_ok=True)

        file_path = os.path.join(
            "uploads/assignments",
            uploaded_pdf.name
        )

        # Save PDF
        with open(file_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        # Database
        conn = sqlite3.connect("teachtwin.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO assignments
        (
            teacher_id,
            title,
            description,
            due_date,
            question_file_name,
            question_file_path,
            created_on
        )

        VALUES(?,?,?,?,?,?,?)
        """, (

            teacher_id,
            title,
            description,
            str(due_date),
            uploaded_pdf.name,
            file_path,
            str(datetime.now())

        ))

        conn.commit()
        conn.close()

        st.success("🎉 Assignment Published Successfully!")
