from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):

    registration_no: str = Field(
        min_length=5,
        max_length=20,
        description="Student registration number"
    )

    password: str = Field(
        min_length=8,
        max_length=64
    )
class UserLoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=64
    )