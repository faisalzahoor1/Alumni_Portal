from typing import List, Optional
from fastapi import HTTPException, status
from app.core.constants import Engagement, Roles
from app.common.identity import get_display_identity
from app.engagement.models.comment import Comment
from app.engagement.repositories.engagement_repository import EngagementRepository
from app.engagement.schemas.engagement_schema import CommentResponse, ReactionSummary
from app.alumni.models.notification import AlumniNotification
from app.alumni.repositories.notification_repository import NotificationRepository


REACTION_VALUES = [r["value"] for r in Engagement.REACTIONS]


class EngagementService:

    @staticmethod
    async def _get_post_or_404(post_id: str) -> dict:
        post = await EngagementRepository.get_public_post(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post

    @staticmethod
    async def _notify_alumni(recipient_id: str, recipient_role: str, actor: dict, title: str, message: str, post_id: str):
        """Alumni have a notification inbox; skip other roles and self-actions."""
        if recipient_role != Roles.ALUMNI or recipient_id == actor["id"]:
            return
        await NotificationRepository.create_notification(
            AlumniNotification(recipient_id=recipient_id, title=title, message=message, type="post", related_entity_id=post_id)
        )

    @staticmethod
    async def set_reaction(post_id: str, entity: dict, reaction: Optional[str]) -> ReactionSummary:
        await EngagementService._get_post_or_404(post_id)
        await EngagementRepository.set_reaction(post_id, entity["id"], reaction)
        counts = await EngagementRepository.refresh_counts(post_id, REACTION_VALUES)
        return ReactionSummary(
            post_id=post_id,
            likes_count=counts.get("likes_count", 0),
            dislikes_count=counts.get("dislikes_count", 0),
            my_reaction=reaction
        )

    @staticmethod
    async def get_comments(post_id: str, viewer: Optional[dict], limit: int, skip: int) -> List[CommentResponse]:
        await EngagementService._get_post_or_404(post_id)
        comments = await EngagementRepository.get_comments(post_id, limit, skip)
        viewer_id = viewer["id"] if viewer else None
        return [CommentResponse(**c.model_dump(), is_mine=c.author_id == viewer_id) for c in comments]

    @staticmethod
    async def add_comment(post_id: str, entity: dict, content: str, parent_id: Optional[str] = None) -> CommentResponse:
        post = await EngagementService._get_post_or_404(post_id)

        parent = None
        if parent_id:
            parent = await EngagementRepository.get_comment(post_id, parent_id)
            if not parent:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment to reply to was not found")
            # Threads are one level deep: a reply to a reply joins the same thread
            parent_id = parent.parent_id or parent.id

        identity = await get_display_identity(entity)
        comment = await EngagementRepository.create_comment(
            Comment(
                post_id=post_id,
                parent_id=parent_id,
                author_id=entity["id"],
                author_name=identity["name"],
                author_role=entity["role"],
                author_avatar=identity["avatar_url"],
                content=content
            )
        )
        await EngagementRepository.refresh_counts(post_id, REACTION_VALUES)

        title = post.get("title", "your post")
        if parent:
            await EngagementService._notify_alumni(
                parent.author_id, parent.author_role, entity,
                "New reply to your comment", f'{identity["name"]} replied on "{title}": {content[:120]}', post_id
            )
        if not parent or parent.author_id != post.get("author_id"):
            await EngagementService._notify_alumni(
                post.get("author_id"), post.get("author_role"), entity,
                "New comment on your post", f'{identity["name"]} commented on "{title}": {content[:120]}', post_id
            )

        return CommentResponse(**comment.model_dump(), is_mine=True)

    @staticmethod
    async def delete_comment(post_id: str, comment_id: str, entity: dict) -> dict:
        deleted = await EngagementRepository.delete_comment(post_id, comment_id, entity["id"])
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        await EngagementRepository.refresh_counts(post_id, REACTION_VALUES)
        return {"message": "Comment deleted"}

    @staticmethod
    async def attach_my_reactions(posts: list, user_id: str) -> list:
        """Fill in `my_reaction` on feed posts for the current viewer."""
        if not posts:
            return posts
        mine = await EngagementRepository.get_reactions_for_user([p.id for p in posts], user_id)
        for post in posts:
            post.my_reaction = mine.get(post.id)
        return posts
