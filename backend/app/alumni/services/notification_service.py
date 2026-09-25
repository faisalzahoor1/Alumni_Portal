from typing import List
from fastapi import HTTPException, status
from app.alumni.repositories.notification_repository import NotificationRepository
from app.alumni.schemas.notification_schema import NotificationResponse


class NotificationService:

    @staticmethod
    async def get_notifications(
        recipient_id: str,
        unread_only: bool = False,
        limit: int = 50,
        skip: int = 0
    ) -> List[NotificationResponse]:
        notifications = await NotificationRepository.get_all_for_recipient(
            recipient_id=recipient_id,
            unread_only=unread_only,
            limit=limit,
            skip=skip
        )
        return [NotificationResponse(**n.model_dump()) for n in notifications]

    @staticmethod
    async def get_unread_count(recipient_id: str) -> int:
        return await NotificationRepository.count_unread(recipient_id=recipient_id)

    @staticmethod
    async def mark_as_read(notification_id: str, recipient_id: str) -> NotificationResponse:
        notification = await NotificationRepository.mark_as_read(
            notification_id=notification_id,
            recipient_id=recipient_id
        )
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return NotificationResponse(**notification.model_dump())

    @staticmethod
    async def mark_all_as_read(recipient_id: str) -> dict:
        count = await NotificationRepository.mark_all_as_read(recipient_id=recipient_id)
        return {"message": "All notifications marked as read", "modified_count": count}

    @staticmethod
    async def delete_notification(notification_id: str, recipient_id: str) -> dict:
        deleted = await NotificationRepository.delete_notification(
            notification_id=notification_id,
            recipient_id=recipient_id
        )
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return {"message": "Notification deleted successfully"}
