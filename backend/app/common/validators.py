from pydantic import EmailStr
from pydantic import HttpUrl
from pydantic import BaseModel


class AdditionalInfoValidator(BaseModel):

    email: EmailStr

    linkedin: HttpUrl

    instagram: HttpUrl