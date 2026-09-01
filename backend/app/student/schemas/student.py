from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime

class CVResponse(BaseModel):

    file_name: str

    file_url: str

    file_size: int

    content_type: str

    uploaded_at: datetime


class StudentResponse(BaseModel):

    id: str

    registration_no: str

    name: str

    email: EmailStr

    linkedin_url: HttpUrl | None = None

    instagram_url: HttpUrl | None = None

    cv: CVResponse | None = None
