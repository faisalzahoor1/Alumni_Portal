from datetime import datetime, timezone
from typing import Optional
from app.database import mongodb
from app.database.collections import Collections
from app.alumni.models.alumni import AlumniProfile


class AlumniProfileRepository:

    @staticmethod
    async def create_profile(profile: AlumniProfile) -> str:
        profile_dict = profile.model_dump()
        result = await mongodb.database[Collections.ALUMNI_PROFILES].insert_one(profile_dict)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_user_id(user_id: str) -> Optional[AlumniProfile]:
        document = await mongodb.database[Collections.ALUMNI_PROFILES].find_one({"user_id": user_id})
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        return AlumniProfile(**document)

    @staticmethod
    async def update_profile(user_id: str, update_data: dict) -> Optional[AlumniProfile]:
        update_data["updated_at"] = datetime.now(timezone.utc)
        await mongodb.database[Collections.ALUMNI_PROFILES].update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        return await AlumniProfileRepository.get_by_user_id(user_id)
