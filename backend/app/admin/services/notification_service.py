from typing import List
from fastapi import HTTPException, status
from app.admin.models.admin_notification import AdminNotification
from app.admin.repositories.notification_repository import AdminNotificationRepository


class AdminNotificationService:

    @staticmethod
    async def notify(title: str, message: str, type: str, related_entity_id: str | None = None):
        await AdminNotificationRepository.create(
            AdminNotification(title=title, message=message, type=type, related_entity_id=related_entity_id)
        )

    @staticmethod
    async def list(unread_only: bool, limit: int, skip: int) -> List[AdminNotification]:
        return await AdminNotificationRepository.list(unread_only, limit, skip)

    @staticmethod
    async def unread_count() -> int:
        return await AdminNotificationRepository.count_unread()

    @staticmethod
    async def mark_read(notification_id: str) -> dict:
        if not await AdminNotificationRepository.mark_read(notification_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return {"message": "Marked as read"}

    @staticmethod
    async def mark_all_read() -> dict:
        await AdminNotificationRepository.mark_all_read()
        return {"message": "All notifications marked as read"}

    @staticmethod
    async def delete(notification_id: str) -> dict:
        if not await AdminNotificationRepository.delete(notification_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return {"message": "Notification deleted"}
