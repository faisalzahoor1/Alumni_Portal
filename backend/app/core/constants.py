# app/core/constants.py

class Roles:
    STUDENT = "student"
    ALUMNI = "alumni"
    INDUSTRY = "industry"
    ADMIN = "admin"


class TokenType:
    ACCESS = "access"
    REFRESH = "refresh"

class OTP:
    LENGTH = 6                 # OTP will have 6 digits
    EXPIRY_SECONDS = 60       # Expires after 5 minutes


class RedisKeys:
    OTP = "otp"