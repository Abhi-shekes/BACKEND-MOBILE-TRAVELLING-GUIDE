import smtplib
from email.mime.text import MIMEText
import pyotp

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'toursarthiservices@gmail.com'
SMTP_PASSWORD = 'tqzxpmvyyoxdsdrv'

OTP_TO_EMAIL = {}


def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), digits=6)
    return totp.now()


def send_otp_email(email):
    try:
        otp = generate_otp()
        OTP_TO_EMAIL[email] = otp
        print(f"OTP_TO_EMAIL = {OTP_TO_EMAIL}")
        msg = MIMEText(f'Your OTP is: {otp}')
        msg['Subject'] = 'OTP Verification'
        msg['From'] = SMTP_USERNAME
        msg['To'] = email

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        server.sendmail(SMTP_USERNAME, [email], msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print(str(e))
        return False

