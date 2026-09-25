from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class AlumniProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    graduation_year: Optional[int] = None
    degree: Optional[str] = None
    department: Optional[str] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    skills: Optional[List[str]] = None
    achievements: Optional[List[str]] = None
    phone: Optional[str] = None


class AlumniProfileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: str
    user_id: str
    name: str
    email: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    graduation_year: Optional[int] = None
    degree: Optional[str] = None
    department: Optional[str] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    skills: List[str] = []
    achievements: List[str] = []
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime
