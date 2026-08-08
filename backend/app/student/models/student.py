from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Student(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    id: str | None = None

    registration_no: str

    name: str

    email: EmailStr

    linkedin_url: str | None = None

    instagram_url: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )