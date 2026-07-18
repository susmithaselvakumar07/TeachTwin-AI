import streamlit as st
import sqlite3
import os

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="wide"
)

st.title("📥 Student Assignment Submissions")

# -----------------------------
# Login Check
# -----------------------------
teacher_id = st.session_state.get("teacher_id")

if not teacher_id:
    st.error("Please login first.")
    st.stop()

# -----------------------------
# Database
# -----------------------------
conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

# -----------------------------
# Get Teacher Assignments
# -----------------------------
cursor.execute("""
SELECT
id,
title
FROM assignments
WHERE teacher_id=?
ORDER BY id DESC
""", (teacher_id,))

assignments = cursor.fetchall()

if len(assignments) == 0:
    st.info("No assignments created yet.")
    conn.close()
    st.stop()

# -----------------------------
# Display Assignments
# -----------------------------
for assignment in assignments:

    assignment_id = assignment[0]

    st.subheader(f"📝 {assignment[1]}")

    cursor.execute("""
    SELECT
    student_name,
    student_email,
    file_name,
    file_path,
    submitted_on
    FROM submissions
    WHERE assignment_id=?
    ORDER BY submitted_on DESC
    """, (assignment_id,))

    submissions = cursor.fetchall()

    if len(submissions) == 0:

        st.warning("No submissions yet.")

    else:

        for sub in submissions:

            with st.container():

                st.markdown(f"""
### 👨‍🎓 {sub[0]}

📧 **Email:** {sub[1]}

📅 **Submitted On:** {sub[4]}
""")

                if os.path.exists(sub[3]):

                    with open(sub[3], "rb") as file:

                        st.download_button(
                            "⬇ Download Submission",
                            file,
                            file_name=sub[2],
                            key=f"{assignment_id}_{sub[1]}"
                        )

                st.divider()

conn.close()
