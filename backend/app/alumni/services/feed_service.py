from typing import Optional, List
from fastapi import HTTPException, status
from app.alumni.repositories.post_repository import PostRepository
from app.alumni.models.post import Post
from app.alumni.schemas.feed_schema import FeedResponse
from app.alumni.schemas.post_schema import PostResponse


class FeedService:

    @staticmethod
    async def get_feed(
        post_type: Optional[str] = None,
        author_role: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> FeedResponse:
        roles: Optional[List[str]] = [author_role] if author_role else ["alumni", "industry"]
        skip = (page - 1) * limit

        posts = await PostRepository.get_feed(
            roles=roles,
            post_type=post_type,
            search=search,
            limit=limit,
            skip=skip
        )
        total = await PostRepository.count_feed(
            roles=roles,
            post_type=post_type,
            search=search
        )

        post_responses = [PostResponse(**post.model_dump()) for post in posts]
        has_more = (skip + len(posts)) < total

        return FeedResponse(
            posts=post_responses,
            total=total,
            page=page,
            limit=limit,
            has_more=has_more
        )

    @staticmethod
    async def get_feed_post(post_id: str) -> PostResponse:
        post = await PostRepository.get_by_id(post_id)
        if not post or not post.is_public:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found in community feed"
            )
        return PostResponse(**post.model_dump())
