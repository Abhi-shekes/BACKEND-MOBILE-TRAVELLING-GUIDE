from reset_password import OTP_TO_EMAIL


def validate_otp(email, entered_otp):
    stored_otp = OTP_TO_EMAIL.get(email)
    if stored_otp and stored_otp == entered_otp:
        return True
    else:
        return False
