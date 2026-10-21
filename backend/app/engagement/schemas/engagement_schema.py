from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from app.core.constants import Engagement


class ReactionRequest(BaseModel):
    reaction: Optional[str] = None  # null removes the viewer's reaction

    @field_validator("reaction")
    @classmethod
    def validate_reaction(cls, reaction: Optional[str]):
        allowed = [r["value"] for r in Engagement.REACTIONS]
        if reaction is not None and reaction not in allowed:
            raise ValueError(f"Reaction must be one of: {', '.join(allowed)}")
        return reaction


class ReactionSummary(BaseModel):
    post_id: str
    likes_count: int
    dislikes_count: int
    my_reaction: Optional[str] = None


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=Engagement.COMMENT_MAX_LENGTH)
    parent_id: Optional[str] = None  # reply to this comment

    @field_validator("content")
    @classmethod
    def strip_content(cls, content: str):
        content = content.strip()
        if not content:
            raise ValueError("Comment cannot be empty")
        return content


class CommentResponse(BaseModel):
    id: str
    post_id: str
    parent_id: Optional[str] = None
    author_id: str
    author_name: str
    author_role: str
    author_avatar: Optional[str] = None
    content: str
    created_at: datetime
    is_mine: bool = False
