import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import dotenv_values

# ------------------------------------
# Load .env
# ------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

config = dotenv_values(BASE_DIR / ".env")

sender_email = config.get("MAIL_ID")
password = config.get("PASSWORD")

# Debug (Remove after testing)
print("Sender Email:", sender_email)
print("Password Loaded:", "YES" if password else "NO")


# ------------------------------------
# Send OTP Email
# ------------------------------------
def send_otp(receiver_email, otp):

    # Safety check
    if not sender_email or not password:
        raise Exception(
            "MAIL_ID or PASSWORD not found in .env"
        )

    msg = EmailMessage()

    msg["Subject"] = "TeachTwin AI - OTP Verification"

    msg["From"] = sender_email

    msg["To"] = receiver_email

    msg.set_content(f"""
Hello,

Your TeachTwin AI verification OTP is:

{otp}

This OTP is valid for 5 minutes.

Please do not share this OTP with anyone.

Thank you,
TeachTwin AI Team
""")

    try:

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

            server.login(sender_email, password)

            server.send_message(msg)

        return True

    except Exception as e:

        print("Email Sending Error:", e)

        return False