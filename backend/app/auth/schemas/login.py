from pydantic import BaseModel


class LoginRequest(BaseModel):

    registration_no: str

    password: str