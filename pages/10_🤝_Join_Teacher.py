import streamlit as st
import sqlite3

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="centered"
)

st.title("🤝 Join Your Teacher")

# -----------------------------
# Login Check
# -----------------------------
student_email = st.session_state.get("student_email")

if not student_email:
    st.error("Please login first.")
    st.stop()

st.write(f"👤 Logged in as: {student_email}")

st.write("")

teacher_id_input = st.text_input("🆔 Enter TeachTwin ID")

st.write("")

# -----------------------------
# Find Teacher
# -----------------------------
if st.button("🔍 Find Teacher", use_container_width=True):

    if teacher_id_input.strip() == "":
        st.error("Please enter TeachTwin ID.")

    else:

        conn = sqlite3.connect("teachtwin.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT full_name, subject, department
            FROM teachers
            WHERE teachtwin_id=?
        """, (teacher_id_input,))

        teacher = cursor.fetchone()

        conn.close()

        if teacher:
            st.session_state["found_teacher"] = teacher
            st.session_state["found_teacher_id"] = teacher_id_input
        else:
            st.error("❌ Teacher not found.")

# -----------------------------
# Show Teacher Details
# -----------------------------
if "found_teacher" in st.session_state:

    teacher = st.session_state["found_teacher"]
    teacher_id = st.session_state["found_teacher_id"]

    st.success("✅ Teacher Found!")

    st.write(f"### 👨‍🏫 {teacher[0]}")
    st.write(f"**📚 Subject:** {teacher[1]}")
    st.write(f"**🏢 Department:** {teacher[2]}")

    st.write("")

    if st.button("✅ Join Teacher", use_container_width=True):

        conn = sqlite3.connect("teachtwin.db")
        cursor = conn.cursor()

        # Check if already connected
        cursor.execute("""
        SELECT *
        FROM student_teacher
        WHERE student_email=? AND teacher_id=?
        """, (student_email, teacher_id))

        already = cursor.fetchone()

        if already:

            conn.close()

            st.success("✅ You are already connected with this teacher.")

            del st.session_state["found_teacher"]
            del st.session_state["found_teacher_id"]

            st.switch_page("pages/11_🎓_Student_Dashboard.py")

        else:

            cursor.execute("""
            INSERT INTO student_teacher
            (student_email, teacher_id)
            VALUES (?, ?)
            """, (student_email, teacher_id))

            conn.commit()
            conn.close()

            st.success("🎉 Successfully Connected to your Teacher!")

            del st.session_state["found_teacher"]
            del st.session_state["found_teacher_id"]

            st.switch_page("pages/11_🎓_Student_Dashboard.py")
