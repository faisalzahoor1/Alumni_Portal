from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class Comment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[str] = None
    post_id: str
    parent_id: Optional[str] = None  # set on replies; always a top-level comment
    author_id: str
    author_name: str
    author_role: str
    author_avatar: Optional[str] = None
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
