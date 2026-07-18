import streamlit as st
import sqlite3
from database.database import initialize_database

initialize_database()


st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="centered"
)

# -------------------------
# Redirect if already logged in
# -------------------------
if st.session_state.get("student_logged_in", False):
    st.switch_page("pages/11_🎓_Student_Dashboard.py")

# -------------------------
# Top Right Logo
# -------------------------
left, right = st.columns([9, 1])

with right:
    st.image("favicon.png", width=55)

# -------------------------
# Heading
# -------------------------
st.markdown(
    "<h1 style='text-align:center;'>🎓 Welcome Back!</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Sign in to continue learning with TeachTwin AI.</h4>",
    unsafe_allow_html=True
)

st.write("")

email = st.text_input("📧 Email Address")

password = st.text_input("🔒 Password", type="password")

st.write("")

# -------------------------
# Login Button
# -------------------------
if st.button("🔑 Sign In", use_container_width=True):

    if email == "" or password == "":
        st.error("Please enter Email and Password.")

    else:

        conn = sqlite3.connect("teachtwin.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT full_name,
               email,
               password,
               department,
               college
        FROM students
        WHERE email=?
        """, (email,))

        student = cursor.fetchone()

        conn.close()

        if student is None:
            st.error("No account found with this email.")

        elif student[2] != password:
            st.error("Incorrect Password.")

        else:

            # Save session
            st.session_state.student_logged_in = True
            st.session_state.student_name = student[0]
            st.session_state.student_email = student[1]
            st.session_state.student_department = student[3]
            st.session_state.student_college = student[4]

            # Check Teacher Connection
            conn = sqlite3.connect("teachtwin.db")
            cursor = conn.cursor()

            cursor.execute("""
            SELECT *
            FROM student_teacher
            WHERE student_email=?
            """, (student[1],))

            connection = cursor.fetchone()

            conn.close()

            if connection:
                st.switch_page("pages/11_🎓_Student_Dashboard.py")
            else:
                st.switch_page("pages/10_🤝_Join_Teacher.py")

st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Create Account", use_container_width=True):
        st.switch_page("pages/7_📝_Student_SignUp.py")

with col2:
    if st.button("🔒 Forgot Password", use_container_width=True):
        st.switch_page("pages/17_🔑_Forgot_Password.py")
