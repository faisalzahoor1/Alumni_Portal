from pydantic import BaseModel, HttpUrl


class StudentAdditionalInfoRequest(BaseModel):

    linkedin_url: HttpUrl | None = None

    instagram_url: HttpUrl | None = None