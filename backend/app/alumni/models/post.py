from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class Post(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[str] = None
    author_id: str
    author_name: str
    author_role: str = "alumni"  # "alumni" | "industry"
    author_avatar: Optional[str] = None
    title: str
    content: str
    media_urls: List[str] = Field(default_factory=list)  # pictures of achievements, etc.
    job_apply_url: Optional[str] = None  # application forms or job links
    external_urls: List[str] = Field(default_factory=list)  # additional URLs
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    post_type: str = "general"  # "achievement", "job_opportunity", "announcement", "general"
    tags: List[str] = Field(default_factory=list)
    likes_count: int = 0
    comments_count: int = 0
    is_public: bool = True  # Visible in feed

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
