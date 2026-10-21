from typing import List
from bson import ObjectId
import pymongo
from app.database import mongodb
from app.database.collections import Collections
from app.admin.models.admin_notification import AdminNotification


class AdminNotificationRepository:

    @staticmethod
    async def create(notification: AdminNotification) -> AdminNotification:
        result = await mongodb.database[Collections.ADMIN_NOTIFICATIONS].insert_one(notification.model_dump(exclude={"id"}))
        notification.id = str(result.inserted_id)
        return notification

    @staticmethod
    async def list(unread_only: bool, limit: int, skip: int) -> List[AdminNotification]:
        query = {"is_read": False} if unread_only else {}
        cursor = (
            mongodb.database[Collections.ADMIN_NOTIFICATIONS]
            .find(query)
            .sort("created_at", pymongo.DESCENDING)
            .skip(skip)
            .limit(limit)
        )
        items = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            items.append(AdminNotification(**doc))
        return items

    @staticmethod
    async def count_unread() -> int:
        return await mongodb.database[Collections.ADMIN_NOTIFICATIONS].count_documents({"is_read": False})

    @staticmethod
    async def mark_read(notification_id: str) -> bool:
        if not ObjectId.is_valid(notification_id):
            return False
        result = await mongodb.database[Collections.ADMIN_NOTIFICATIONS].update_one(
            {"_id": ObjectId(notification_id)}, {"$set": {"is_read": True}}
        )
        return result.matched_count > 0

    @staticmethod
    async def mark_all_read():
        await mongodb.database[Collections.ADMIN_NOTIFICATIONS].update_many({"is_read": False}, {"$set": {"is_read": True}})

    @staticmethod
    async def delete(notification_id: str) -> bool:
        if not ObjectId.is_valid(notification_id):
            return False
        result = await mongodb.database[Collections.ADMIN_NOTIFICATIONS].delete_one({"_id": ObjectId(notification_id)})
        return result.deleted_count > 0
