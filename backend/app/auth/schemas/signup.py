from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from app.core.constants import Password, Roles


class SignupRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=Password.MIN_LENGTH,
        max_length=Password.MAX_LENGTH
    )

    confirm_password: str

    role: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, role: str):
        allowed = [r["value"] for r in Roles.SIGNUP]
        if role not in allowed:
            raise ValueError(f"Role must be one of: {', '.join(allowed)}")
        return role

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class SignupResponse(BaseModel):
    message: str