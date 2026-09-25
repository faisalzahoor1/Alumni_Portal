from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.auth.dependensies import get_current_authenticated_entity
from app.alumni.schemas.feed_schema import FeedResponse
from app.alumni.schemas.post_schema import PostResponse
from app.alumni.services.feed_service import FeedService

router = APIRouter(prefix="/feed", tags=["Community Feed"])


@router.get("/", response_model=FeedResponse)
async def get_community_feed(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    author_role: Optional[str] = Query(None, description="Filter by author role: alumni, industry"),
    post_type: Optional[str] = Query(None, description="Filter by post type: achievement, job_opportunity, general"),
    search: Optional[str] = Query(None, description="Search query across posts"),
    current_entity: dict = Depends(get_current_authenticated_entity)
):
    """
    Public community feed accessible to all authenticated roles (Students, Alumni, Industry).
    Displays posts from both Alumni and Industry users.
    """
    return await FeedService.get_feed(
        post_type=post_type,
        author_role=author_role,
        search=search,
        page=page,
        limit=limit
    )


@router.get("/{post_id}", response_model=PostResponse)
async def get_feed_post(
    post_id: str,
    current_entity: dict = Depends(get_current_authenticated_entity)
):
    """View details of a specific community feed post."""
    return await FeedService.get_feed_post(post_id=post_id)
