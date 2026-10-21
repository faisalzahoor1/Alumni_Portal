from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.auth.dependensies import get_feed_viewer
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
    viewer: Optional[dict] = Depends(get_feed_viewer)
):
    """
    Community feed for every role, and for logged-out visitors while Feed.PUBLIC is on.
    Displays posts from both Alumni and Industry users.
    """
    return await FeedService.get_feed(
        post_type=post_type,
        author_role=author_role,
        search=search,
        page=page,
        limit=limit,
        viewer_id=viewer["id"] if viewer else None
    )


@router.get("/{post_id}", response_model=PostResponse)
async def get_feed_post(
    post_id: str,
    viewer: Optional[dict] = Depends(get_feed_viewer)
):
    """View details of a specific community feed post."""
    return await FeedService.get_feed_post(post_id=post_id, viewer_id=viewer["id"] if viewer else None)
