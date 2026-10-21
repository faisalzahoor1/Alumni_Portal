from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.auth.dependensies import get_feed_viewer, require_entity
from app.core.constants import Reports, University
from app.alumni.schemas.feed_schema import FeedResponse
from app.alumni.services.feed_service import FeedService
from app.admin.schemas.admin_schema import ReportCreate
from app.admin.services.report_service import ReportService

router = APIRouter(tags=["University Posts & Reports"])


@router.get("/university-posts/", response_model=FeedResponse)
async def get_university_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    post_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    viewer: Optional[dict] = Depends(get_feed_viewer)
):
    """Official university posts for every role (and visitors while the feed is public)."""
    return await FeedService.get_feed(
        post_type=post_type,
        author_role=University.AUTHOR_ROLE,
        search=search,
        page=page,
        limit=limit,
        viewer_id=viewer["id"] if viewer else None
    )


get_reporting_entity = require_entity(Reports.ROLES, True, "report posts")


@router.post("/posts/{post_id}/report")
async def report_post(post_id: str, request: ReportCreate, entity: dict = Depends(get_reporting_entity)):
    """Flag a post for admin review."""
    return await ReportService.submit(post_id, entity, request.reason, request.details)
