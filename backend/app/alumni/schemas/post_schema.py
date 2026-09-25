from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=250)
    content: str = Field(..., min_length=1)
    media_urls: Optional[List[str]] = []
    job_apply_url: Optional[str] = None
    external_urls: Optional[List[str]] = []
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    post_type: Optional[str] = "general"  # "achievement", "job_opportunity", "announcement", "general"
    tags: Optional[List[str]] = []
    is_public: Optional[bool] = True


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=250)
    content: Optional[str] = Field(None, min_length=1)
    media_urls: Optional[List[str]] = None
    job_apply_url: Optional[str] = None
    external_urls: Optional[List[str]] = None
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    post_type: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None


class PostResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: str
    author_id: str
    author_name: str
    author_role: str
    author_avatar: Optional[str] = None
    title: str
    content: str
    media_urls: List[str] = []
    job_apply_url: Optional[str] = None
    external_urls: List[str] = []
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    post_type: str
    tags: List[str] = []
    likes_count: int = 0
    comments_count: int = 0
    is_public: bool = True
    created_at: datetime
    updated_at: datetime


class MediaUploadResponse(BaseModel):
    file_url: str
    file_name: Optional[str] = None
