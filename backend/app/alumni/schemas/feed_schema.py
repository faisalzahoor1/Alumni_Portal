from typing import List
from pydantic import BaseModel
from app.alumni.schemas.post_schema import PostResponse


class FeedResponse(BaseModel):
    posts: List[PostResponse]
    total: int
    page: int
    limit: int
    has_more: bool
