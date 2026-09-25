from typing import List
from pydantic import BaseModel
from app.industry.schemas.post_schema import PostResponse


class IndustryFeedResponse(BaseModel):
    posts: List[PostResponse]
    total: int
    page: int
    limit: int
    has_more: bool


# Alias for consistency
FeedResponse = IndustryFeedResponse
