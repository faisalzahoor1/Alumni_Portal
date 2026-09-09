from typing import List, Optional
from fastapi import HTTPException, status

from app.industry.models.notification import IndustryNotification
from app.industry.schemas.notification_schema import NotificationCreate
from app.industry.repositories.notification_repository import NotificationRepository


class NotificationService:

    @staticmethod
    async def create_notification(data: NotificationCreate) -> IndustryNotification:
        notification = IndustryNotification(**data.model_dump())
        return await NotificationRepository.create_notification(notification)

    @staticmethod
    async def get_notifications(
        recipient_id: str,
        unread_only: bool = False,
        limit: int = 50,
        skip: int = 0
    ) -> List[IndustryNotification]:
        return await NotificationRepository.get_all_for_recipient(
            recipient_id=recipient_id,
            unread_only=unread_only,
            limit=limit,
            skip=skip
        )

    @staticmethod
    async def get_unread_count(recipient_id: str) -> int:
        return await NotificationRepository.count_unread(recipient_id)

    @staticmethod
    async def mark_as_read(notification_id: str, recipient_id: str) -> IndustryNotification:
        notification = await NotificationRepository.mark_as_read(notification_id, recipient_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return notification

    @staticmethod
    async def mark_all_as_read(recipient_id: str) -> dict:
        count = await NotificationRepository.mark_all_as_read(recipient_id)
        return {"message": f"{count} notifications marked as read", "updated_count": count}

    @staticmethod
    async def delete_notification(notification_id: str, recipient_id: str) -> dict:
        deleted = await NotificationRepository.delete_notification(notification_id, recipient_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return {"message": "Notification deleted successfully"}
