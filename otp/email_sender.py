import smtplib
import streamlit as st
from email.mime.text import MIMEText
from dotenv import dotenv_values

# Try local .env first
config = dotenv_values(".env")

MAIL_ID = config.get("MAIL_ID")
PASSWORD = config.get("PASSWORD")

# If running on Streamlit Cloud, use Secrets
if not MAIL_ID or not PASSWORD:
    MAIL_ID = st.secrets.get("MAIL_ID")
    PASSWORD = st.secrets.get("PASSWORD")


def send_otp(receiver_email, otp):

    if not MAIL_ID or not PASSWORD:
        raise Exception(
            "MAIL_ID or PASSWORD not found in environment settings."
        )

    subject = "TeachTwin AI - OTP Verification"

    body = f"""
Hello,

Your TeachTwin AI OTP is:

{otp}

This OTP is valid for verification.

Thank you,
TeachTwin AI
"""

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = MAIL_ID
    message["To"] = receiver_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.starttls()

        server.login(MAIL_ID, PASSWORD)

        server.sendmail(
            MAIL_ID,
            receiver_email,
            message.as_string()
        )