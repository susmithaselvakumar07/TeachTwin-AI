import streamlit as st
import sqlite3
from otp.otp_generator import generate_otp
from otp.email_sender import send_otp
from database.id_generator import generate_teachtwin_id
st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="centered"
)

# Top-right logo
left, right = st.columns([9, 1])

with right:
    st.image("favicon.png", width=55)

st.markdown(
    "<h1 style='text-align:center;'>📝 Create Your AI Twin</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Create your TeachTwin AI account and start your personalized teaching journey.</h4>",
    unsafe_allow_html=True
)

st.write("")

name = st.text_input("👤 Full Name")

email = st.text_input("📧 Email Address")

password = st.text_input("🔒 Password", type="password")

confirm = st.text_input("🔒 Confirm Password", type="password")

subject = st.selectbox(
    "📚 Select Subject",
    [
        "Artificial Intelligence",
        "Machine Learning",
        "Deep Learning",
        "Data Science",
        "Computer Science Engineering",
        "Information Technology",
        "Cyber Security",
        "Cloud Computing",
        "Web Development",
        "Python Programming",
        "Java Programming",
        "Data Structures",
        "Database Management Systems",
        "Operating Systems",
        "Computer Networks",
        "Software Engineering",
        "Mathematics",
        "Physics",
        "Chemistry",
        "English",
        "Commerce",
        "Other"
    ]
)
department = st.selectbox(
    "🏢 Department",
    [
        "CSE",
        "IT",
        "AIDS",
        "ECE",
        "EEE",
        "MECH",
        "CIVIL",
        "MBA",
        "BCA",
        "MCA"
    ]
)
institution = st.text_input("🏫 Institution / College")

st.write("")
# -----------------------------
# OTP Session Variables
# -----------------------------
if "teacher_signup_otp" not in st.session_state:
    st.session_state.teacher_signup_otp = None

if "teacher_signup_data" not in st.session_state:
    st.session_state.teacher_signup_data = None

if "teacher_otp_sent" not in st.session_state:
    st.session_state.teacher_otp_sent = False
if st.button("🚀 Create Account", use_container_width=True):

    # Validation
    if not all([name, email, password, confirm, institution]):
        st.error("Please fill all the fields.")

    elif password != confirm:
        st.error("Passwords do not match.")

    else:

        conn = sqlite3.connect("teachtwin.db")
        cursor = conn.cursor()

        # Check existing email
        cursor.execute(
            "SELECT * FROM teachers WHERE email=?",
            (email,)
        )

        existing = cursor.fetchone()

        if existing:
            st.error("Email already exists.")

        else:
            otp = generate_otp()

            send_otp(email,otp)

            st.session_state.teacher_signup_otp = otp

            st.session_state.teacher_signup_data = {
            "name": name,
            "email": email,
            "password": password,
            "department": department,
            "subject": subject
            }

            st.session_state.teacher_otp_sent = True

            st.success("✅ OTP sent to your email.")
            
            conn.close()
# -----------------------------
# OTP Verification
# -----------------------------
if st.session_state.teacher_otp_sent:

    st.divider()

    st.subheader("📩 Verify OTP")

    entered_otp = st.text_input("Enter 6-digit OTP")

    if st.button("✅ Verify OTP", use_container_width=True):

        if entered_otp == st.session_state.teacher_signup_otp:

            data = st.session_state.teacher_signup_data

            teacher_id = generate_teachtwin_id(data["department"])

            conn = sqlite3.connect("teachtwin.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO teachers
                (full_name, email, password, department, subject, college, teachtwin_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["email"],
                data["password"],
                data["department"],
                data["subject"],
                data["institution"],
                teacher_id
            ))

            conn.commit()
            conn.close()

            st.success("🎉 Account Created Successfully!")
            st.info(f"🆔 Your TeachTwin ID is: {teacher_id}")

            st.session_state.teacher_signup_otp = None
            st.session_state.teacher_signup_data = None
            st.session_state.teacher_otp_sent = False

        else:

            st.error("❌ Invalid OTP")

st.write("")

if st.button("🔑 Already have an account? Sign In", use_container_width=True):
    st.switch_page("pages/6_🔐_Teacher_Login.py")
