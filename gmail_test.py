import smtplib
from dotenv import dotenv_values

config = dotenv_values(".env")

EMAIL = config["MAIL_ID"]
PASSWORD = config["PASSWORD"]

print("Email:", EMAIL)
print("Password Length:", len(PASSWORD))

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(EMAIL, PASSWORD)

    print("✅ Login Successful!")

    server.quit()

except Exception as e:
    print("❌ Error:", e)
