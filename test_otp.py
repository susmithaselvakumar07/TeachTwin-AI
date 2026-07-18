from otp.otp_generator import generate_otp
from otp.email_sender import send_otp


otp = generate_otp()

print("OTP:",otp)


send_otp(
    "lakshmipriyaselvakumar10@gmail.com",
    otp
)

print("Email Sent Successfully")
