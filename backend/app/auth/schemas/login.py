from pydantic import BaseModel, EmailStr, Field

from app.core.constants import Password, RegistrationNo


class LoginRequest(BaseModel):

    registration_no: str = Field(
        min_length=RegistrationNo.MIN_LENGTH,
        max_length=RegistrationNo.MAX_LENGTH,
        description="Student registration number"
    )

    password: str = Field(
        min_length=Password.MIN_LENGTH,
        max_length=Password.MAX_LENGTH
    )
class UserLoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=Password.MIN_LENGTH,
        max_length=Password.MAX_LENGTH
    )