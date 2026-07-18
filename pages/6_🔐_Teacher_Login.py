import streamlit as st
from components.theme import apply_theme
import sqlite3

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="centered"
)
apply_theme()
    
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
    "<h1 style='text-align:center;'>👨‍🏫 Welcome Back!</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Sign in to continue managing your AI Twin.</h4>",
    unsafe_allow_html=True
)

st.write("")

# -------------------------
# Login Fields
# -------------------------
email = st.text_input("📧 Email Address")

password = st.text_input("🔒 Password", type="password")

st.write("")

# -------------------------
# Sign In Button
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
                   subject,
                   teachtwin_id
            FROM teachers
            WHERE email = ?
        """, (email,))

        teacher = cursor.fetchone()

        conn.close()

        if teacher is None:
            st.error("No account found with this email.")

        elif teacher[2] != password:
            st.error("Incorrect Password.")
        else:
            # Store teacher details
            st.session_state.logged_in = True
            st.session_state.teacher_name = teacher[0]
            st.session_state.teacher_email = teacher[1]
            st.session_state.teacher_department = teacher[3]
            st.session_state.teacher_subject = teacher[4]
            st.session_state.teacher_id = teacher[5]

            st.switch_page("pages/9_🏠_Teacher_Dashboard.py")
        
            st.write("")

# -------------------------
# Bottom Buttons
# -------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Create Account", use_container_width=True):
        st.switch_page("pages/5_📝_Teacher_SignUp.py")

with col2:
    if st.button("🔒 Forgot Password", use_container_width=True):
        st.switch_page("pages/17_🔑_Forgot_Password.py")
