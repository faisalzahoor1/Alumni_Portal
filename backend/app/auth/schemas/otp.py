from pydantic import BaseModel, EmailStr, Field

from app.core.constants import OTP


class VerifyOTPRequest(BaseModel):
    email: EmailStr

    otp: str = Field(
        min_length=OTP.LENGTH,
        max_length=OTP.LENGTH
    )