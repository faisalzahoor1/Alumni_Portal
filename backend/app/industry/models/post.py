from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class Post(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[str] = None
    author_id: str
    author_name: str
    author_role: str = "industry"  # "industry" | "alumni"
    author_avatar: Optional[str] = None
    title: str
    content: str
    media_urls: List[str] = Field(default_factory=list)
    job_apply_url: Optional[str] = None
    external_urls: List[str] = Field(default_factory=list)
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    post_type: str = "job_opportunity"  # "job_opportunity", "announcement", "achievement", "general"
    tags: List[str] = Field(default_factory=list)
    likes_count: int = 0
    comments_count: int = 0
    is_public: bool = True

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
