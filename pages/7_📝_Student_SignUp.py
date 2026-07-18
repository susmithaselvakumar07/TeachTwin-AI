import streamlit as st
import sqlite3
from otp.otp_generator import generate_otp
from otp.email_sender import send_otp
st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="centered"
)

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
    "<h1 style='text-align:center;'>🎓 Join TeachTwin AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Create your student account and start learning from your teacher's AI Twin.</h4>",
    unsafe_allow_html=True
)

st.write("")

# -------------------------
# Student Details
# -------------------------
name = st.text_input("👤 Full Name")

email = st.text_input("📧 Email Address")

password = st.text_input("🔒 Password", type="password")

confirm = st.text_input("🔒 Confirm Password", type="password")

college = st.text_input("🏫 College / Institution")

department = st.selectbox(
    "📚 Department",
    [
        "Artificial Intelligence & Data Science",
        "Computer Science Engineering",
        "Information Technology",
        "Electronics and Communication Engineering",
        "Electrical and Electronics Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Biomedical Engineering",
        "Business Administration",
        "Commerce",
        "Mathematics",
        "Physics",
        "Chemistry",
        "English",
        "Other"
    ]
)

teacher_code = st.text_input("🆔 Teacher AI Code")

st.write("")

# -----------------------------
# OTP Session Variables
# -----------------------------
if "student_signup_otp" not in st.session_state:
    st.session_state.student_signup_otp = None

if "student_signup_data" not in st.session_state:
    st.session_state.student_signup_data = None

if "student_otp_sent" not in st.session_state:
    st.session_state.student_otp_sent = False

# -------------------------
# Buttons
# -------------------------
if st.button("🚀 Join TeachTwin AI", use_container_width=True):

    # Validation
    if not all([name, email, password, confirm, college]):
        st.error("Please fill all the fields.")

    elif password != confirm:
        st.error("Passwords do not match.")

    else:

        conn = sqlite3.connect("teachtwin.db")
        cursor = conn.cursor()

        # Check existing email
        cursor.execute(
            "SELECT * FROM students WHERE email=?",
            (email,)
        )

        existing = cursor.fetchone()

        if existing:
            st.error("Email already exists.")

        else:
             otp = generate_otp()

             send_otp(email, otp)

             st.session_state.student_signup_otp = otp

             st.session_state.student_signup_data = {
                "name": name,
                "email": email,
                "password": password,
                "department": department,
                "college": college
            }

             st.session_state.student_otp_sent = True

             st.success("✅ OTP sent to your email.")
            
             conn.close()

# -----------------------------
# OTP Verification
# -----------------------------
if st.session_state.student_otp_sent:

    st.divider()

    st.subheader("📩 Verify OTP")

    entered_otp = st.text_input("Enter 6-digit OTP")

    if st.button("✅ Verify OTP", use_container_width=True):

        if entered_otp == st.session_state.student_signup_otp:

            data = st.session_state.student_signup_data

            conn = sqlite3.connect("teachtwin.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO students
            (full_name,email,password,department,college)
            VALUES(?,?,?,?,?)
            """,(
                data["name"],
                data["email"],
                data["password"],
                data["department"],
                data["college"]
            ))

            conn.commit()
            conn.close()

            st.success("🎉 Student Account Created Successfully!")
            st.info("You can now login using your email and password.")

            st.session_state.student_signup_otp = None
            st.session_state.student_signup_data = None
            st.session_state.student_otp_sent = False

        else:

            st.error("❌ Invalid OTP")
             
st.write("")

if st.button("🔑 Already have an account? Sign In", use_container_width=True):
    st.switch_page("pages/8_🔐_Student_Login.py")
