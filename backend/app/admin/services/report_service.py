from collections import Counter
from typing import List, Optional
from fastapi import HTTPException, status
from app.core.constants import Reports, Roles
from app.common.identity import get_display_identity
from app.admin.models.report import PostReport
from app.admin.repositories.post_repository import AdminPostRepository
from app.admin.repositories.report_repository import ReportRepository
from app.admin.schemas.admin_schema import ReportedPost, ReportItem
from app.admin.services.notification_service import AdminNotificationService
from app.alumni.schemas.post_schema import PostResponse
from app.alumni.models.notification import AlumniNotification
from app.industry.models.notification import IndustryNotification
from app.alumni.repositories.notification_repository import NotificationRepository as AlumniNotificationRepository
from app.industry.repositories.notification_repository import NotificationRepository as IndustryNotificationRepository
from app.engagement.repositories.engagement_repository import EngagementRepository


class ReportService:

    # ---------- Users ----------

    @staticmethod
    async def submit(post_id: str, entity: dict, reason: str, details: Optional[str]) -> dict:
        post = await EngagementRepository.get_public_post(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.get("author_id") == entity["id"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't report your own post")
        if await ReportRepository.find_pending(post_id, entity["id"]):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You've already reported this post. An admin will review it.")

        identity = await get_display_identity(entity)
        await ReportRepository.create(PostReport(
            post_id=post_id,
            reporter_id=entity["id"],
            reporter_role=entity["role"],
            reporter_name=identity["name"],
            reason=reason,
            details=(details or "").strip() or None
        ))

        reason_label = next((r["label"] for r in Reports.REASONS if r["value"] == reason), reason)
        pending = await ReportRepository.count_pending_for_post(post_id)
        await AdminNotificationService.notify(
            title="Post reported",
            message=f'"{post.get("title", "A post")}" by {post.get("author_name", "unknown")} was reported for {reason_label.lower()}'
                    + (f" ({pending} open reports)" if pending > 1 else "") + ".",
            type="report",
            related_entity_id=post_id
        )
        return {"message": "Thanks for letting us know. An admin will review this post."}

    # ---------- Admins ----------

    @staticmethod
    async def list(report_status: str) -> List[ReportedPost]:
        if report_status not in (Reports.PENDING, Reports.DISMISSED, Reports.ACTIONED):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown report status")
        reports = await ReportRepository.list_by_status(report_status)

        grouped: dict[str, list] = {}
        for report in reports:
            grouped.setdefault(report["post_id"], []).append(report)

        result = []
        for post_id, items in grouped.items():
            post = await AdminPostRepository.get(post_id)
            result.append(ReportedPost(
                post_id=post_id,
                post=PostResponse(**post.model_dump()) if post else None,
                report_count=len(items),
                reasons=dict(Counter(r["reason"] for r in items)),
                last_reported_at=max(r["created_at"] for r in items),
                reports=[ReportItem(**r) for r in items]
            ))
        # Most-reported first, then most recent
        result.sort(key=lambda r: (r.report_count, r.last_reported_at), reverse=True)
        return result

    @staticmethod
    async def dismiss(post_id: str) -> dict:
        resolved = await ReportRepository.resolve_for_post(post_id, Reports.DISMISSED)
        if not resolved:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No open reports for this post")
        return {"message": "Post allowed; reports dismissed", "resolved": resolved}

    @staticmethod
    async def remove_post(post_id: str) -> dict:
        post = await AdminPostRepository.get(post_id)
        if not post:
            await ReportRepository.resolve_for_post(post_id, Reports.ACTIONED)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no longer exists")

        await AdminPostRepository.delete_with_engagement(post_id)
        resolved = await ReportRepository.resolve_for_post(post_id, Reports.ACTIONED)

        notice = {
            "recipient_id": post.author_id,
            "title": "Your post was removed",
            "message": f'An admin removed "{post.title}" after it was reported for breaking community guidelines.',
            "type": "system",
        }
        if post.author_role == Roles.ALUMNI:
            await AlumniNotificationRepository.create_notification(AlumniNotification(**notice))
        elif post.author_role == Roles.INDUSTRY:
            await IndustryNotificationRepository.create_notification(IndustryNotification(**notice))

        return {"message": "Post deleted", "resolved": resolved}
