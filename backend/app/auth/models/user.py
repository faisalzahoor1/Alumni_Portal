from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class User(BaseModel):
        
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
    id: str | None = None

    email: EmailStr

    hashed_password: str

    role: Literal["admin", "alumni", "industry"]

    is_verified: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)