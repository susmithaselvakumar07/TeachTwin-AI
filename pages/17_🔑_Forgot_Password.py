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
    """
    <h1 style='text-align:center;'>
    🔑 Forgot Password
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h4 style='text-align:center;color:gray;'>
    Verify your identity using OTP and create a new password.
    </h4>
    """,
    unsafe_allow_html=True
)

st.write("")

user_type = st.selectbox(
    "👤 Account Type",
    ["Teacher", "Student"]
)

email = st.text_input(
    "📧 Registered Email"
)

# -------------------------
# Session Variables
# -------------------------
if "forgot_otp" not in st.session_state:
    st.session_state.forgot_otp = None

if "forgot_email" not in st.session_state:
    st.session_state.forgot_email = None

if "forgot_table" not in st.session_state:
    st.session_state.forgot_table = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

# -------------------------
# Send OTP
# -------------------------
if st.button("📨 Send OTP", use_container_width=True):

    if email == "":
        st.error("Please enter your email.")

    else:

        table = "teachers" if user_type == "Teacher" else "students"

        conn = sqlite3.connect("teachtwin.db")
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT * FROM {table} WHERE email=?",
            (email,)
        )

        account = cursor.fetchone()

        conn.close()

        if account is None:
            st.error("No account found with this email.")

        else:

            otp = generate_otp()

            send_otp(email, otp)

            st.session_state.forgot_otp = otp
            st.session_state.forgot_email = email
            st.session_state.forgot_table = table

            st.success("✅ OTP sent successfully!")

# -------------------------
# Verify OTP
# -------------------------
if st.session_state.forgot_otp:

    entered = st.text_input("Enter OTP")

    if st.button("✅ Verify OTP", use_container_width=True):

        if entered == st.session_state.forgot_otp:

            st.session_state.otp_verified = True

            st.success("✅ OTP Verified Successfully!")
        else:

            st.error("❌ Invalid OTP")
# -------------------------
# Reset Password
# -------------------------
if st.session_state.otp_verified:

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("🔒 Update Password", use_container_width=True):

        if new_password == "" or confirm_password == "":
            st.error("Please fill all fields.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        else:

            conn = sqlite3.connect("teachtwin.db")
            cursor = conn.cursor()

            cursor.execute(
                f"""
                UPDATE {st.session_state.forgot_table}
                SET password=?
                WHERE email=?
                """,
                (
                    new_password,
                    st.session_state.forgot_email
                )
            )

            conn.commit()
            conn.close()

            st.success("🎉 Password Updated Successfully!")

            st.balloons()
            st.session_state.forgot_otp = None
            st.session_state.forgot_email = None
            st.session_state.forgot_table = None
            st.session_state.otp_verified = False

            st.info("🔐 Please login using your new password.")

            st.write("")
            st.write("")

            st.markdown("---")

            st.markdown(
            """
            <center>
            <b>TeachTwin AI</b><br>
            <span style="color:gray;">
            Your Knowledge. Your AI. Your Students.
            </span>
            </center>
            """,
            unsafe_allow_html=True
        )
