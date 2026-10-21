from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.auth.dependensies import get_feed_viewer, require_entity
from app.core.constants import Engagement
from app.engagement.schemas.engagement_schema import (
    CommentCreate,
    CommentResponse,
    ReactionRequest,
    ReactionSummary,
)
from app.engagement.services.engagement_service import EngagementService

router = APIRouter(prefix="/posts", tags=["Post Engagement"])


get_engaging_entity = require_entity(
    Engagement.ROLES,
    Engagement.REQUIRE_VERIFIED,
    "react to or comment on posts"
)


@router.put("/{post_id}/reaction", response_model=ReactionSummary)
async def set_reaction(
    post_id: str,
    request: ReactionRequest,
    entity: dict = Depends(get_engaging_entity)
):
    """Like, dislike, or clear (reaction: null) a community post."""
    return await EngagementService.set_reaction(post_id, entity, request.reaction)


@router.get("/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    post_id: str,
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    viewer: Optional[dict] = Depends(get_feed_viewer)
):
    """Comments and replies (flat, oldest first; replies carry parent_id). Readable wherever the feed is."""
    return await EngagementService.get_comments(post_id, viewer, limit, skip)


@router.post("/{post_id}/comments", response_model=CommentResponse)
async def add_comment(
    post_id: str,
    request: CommentCreate,
    entity: dict = Depends(get_engaging_entity)
):
    """Comment on a post, or reply to a comment with parent_id."""
    return await EngagementService.add_comment(post_id, entity, request.content, request.parent_id)


@router.delete("/{post_id}/comments/{comment_id}")
async def delete_comment(
    post_id: str,
    comment_id: str,
    entity: dict = Depends(get_engaging_entity)
):
    """Authors can delete their own comments (a comment's replies are removed with it)."""
    return await EngagementService.delete_comment(post_id, comment_id, entity)
