from pydantic import BaseModel, EmailStr, HttpUrl


class StudentResponse(BaseModel):

    id: str

    registration_no: str

    name: str

    email: EmailStr

    linkedin_url: HttpUrl | None = None

    instagram_url: HttpUrl | None = None