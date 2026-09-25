from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.auth.models.user import User
from app.industry.dependecies import get_current_industry_user
from app.industry.schemas.feed import IndustryFeedResponse
from app.industry.schemas.post_schema import PostResponse
from app.industry.services.feed_service import IndustryFeedService

router = APIRouter(prefix="/feed", tags=["Industry Feed"])


@router.get("/", response_model=IndustryFeedResponse)
async def get_community_feed(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    author_role: Optional[str] = Query(None, description="Filter by author role: alumni, industry"),
    post_type: Optional[str] = Query(None, description="Filter by post type: job_opportunity, announcement, achievement, general"),
    search: Optional[str] = Query(None, description="Search term across posts"),
    current_user: User = Depends(get_current_industry_user)
):
    """
    Community feed for industry users: strictly gets posts uploaded by alumni and industry.
    """
    return await IndustryFeedService.get_feed(
        post_type=post_type,
        author_role=author_role,
        search=search,
        page=page,
        limit=limit
    )


@router.get("/{post_id}", response_model=PostResponse)
async def get_feed_post(
    post_id: str,
    current_user: User = Depends(get_current_industry_user)
):
    """View details of a specific community feed post."""
    return await IndustryFeedService.get_post_by_id(post_id=post_id)
