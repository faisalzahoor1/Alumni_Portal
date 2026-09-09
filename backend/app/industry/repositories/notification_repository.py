from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
import pymongo

from app.database import mongodb
from app.database.collections import Collections
from app.industry.models.notification import IndustryNotification


class NotificationRepository:

    @staticmethod
    async def create_notification(notification: IndustryNotification) -> IndustryNotification:
        doc = notification.model_dump()
        result = await mongodb.database[Collections.NOTIFICATIONS].insert_one(doc)
        notification.id = str(result.inserted_id)
        return notification

    @staticmethod
    async def get_by_id(notification_id: str) -> Optional[IndustryNotification]:
        if not ObjectId.is_valid(notification_id):
            return None
        document = await mongodb.database[Collections.NOTIFICATIONS].find_one({"_id": ObjectId(notification_id)})
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        return IndustryNotification(**document)

    @staticmethod
    async def get_all_for_recipient(
        recipient_id: str,
        unread_only: bool = False,
        limit: int = 50,
        skip: int = 0
    ) -> List[IndustryNotification]:
        query = {"recipient_id": recipient_id}
        if unread_only:
            query["is_read"] = False

        cursor = (
            mongodb.database[Collections.NOTIFICATIONS]
            .find(query)
            .sort("created_at", pymongo.DESCENDING)
            .skip(skip)
            .limit(limit)
        )

        notifications = []
        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            notifications.append(IndustryNotification(**document))
        return notifications

    @staticmethod
    async def count_unread(recipient_id: str) -> int:
        return await mongodb.database[Collections.NOTIFICATIONS].count_documents({
            "recipient_id": recipient_id,
            "is_read": False
        })

    @staticmethod
    async def mark_as_read(notification_id: str, recipient_id: str) -> Optional[IndustryNotification]:
        if not ObjectId.is_valid(notification_id):
            return None

        result = await mongodb.database[Collections.NOTIFICATIONS].update_one(
            {"_id": ObjectId(notification_id), "recipient_id": recipient_id},
            {"$set": {"is_read": True}}
        )
        if result.matched_count == 0:
            return None
        return await NotificationRepository.get_by_id(notification_id)

    @staticmethod
    async def mark_all_as_read(recipient_id: str) -> int:
        result = await mongodb.database[Collections.NOTIFICATIONS].update_many(
            {"recipient_id": recipient_id, "is_read": False},
            {"$set": {"is_read": True}}
        )
        return result.modified_count

    @staticmethod
    async def delete_notification(notification_id: str, recipient_id: str) -> bool:
        if not ObjectId.is_valid(notification_id):
            return False

        result = await mongodb.database[Collections.NOTIFICATIONS].delete_one({
            "_id": ObjectId(notification_id),
            "recipient_id": recipient_id
        })
        return result.deleted_count > 0
