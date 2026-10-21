from datetime import datetime, timezone
from typing import Optional
from app.database import mongodb
from app.database.collections import Collections
from app.admin.models.admin_profile import AdminProfile


class AdminProfileRepository:

    @staticmethod
    async def get_by_user_id(user_id: str) -> Optional[AdminProfile]:
        doc = await mongodb.database[Collections.ADMIN_PROFILES].find_one({"user_id": user_id})
        if not doc:
            return None
        doc["id"] = str(doc.pop("_id"))
        return AdminProfile(**doc)

    @staticmethod
    async def create(profile: AdminProfile) -> AdminProfile:
        result = await mongodb.database[Collections.ADMIN_PROFILES].insert_one(profile.model_dump(exclude={"id"}))
        profile.id = str(result.inserted_id)
        return profile

    @staticmethod
    async def update(user_id: str, data: dict) -> Optional[AdminProfile]:
        data["updated_at"] = datetime.now(timezone.utc)
        await mongodb.database[Collections.ADMIN_PROFILES].update_one({"user_id": user_id}, {"$set": data})
        return await AdminProfileRepository.get_by_user_id(user_id)
