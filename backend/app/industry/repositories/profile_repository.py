from app.database import mongodb
from bson import ObjectId
from app.industry.models.industry import IndustryProfile
from app.database.collections import Collections
from datetime import datetime

class IndustryProfileRepository:
    
    @staticmethod
    async def create_profile(profile: IndustryProfile) -> str:
        profile_dict = profile.model_dump()
        result = await mongodb.database[Collections.INDUSTRY_PROFILES].insert_one(profile_dict)
        return str(result.inserted_id)
        
    @staticmethod
    async def get_by_user_id(user_id: str) -> IndustryProfile | None:
        document = await mongodb.database[Collections.INDUSTRY_PROFILES].find_one({"user_id": user_id})
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        return IndustryProfile(**document)

    @staticmethod
    async def update_profile(user_id: str, update_data: dict) -> IndustryProfile | None:
        update_data["updated_at"] = datetime.utcnow()
        await mongodb.database[Collections.INDUSTRY_PROFILES].update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        return await IndustryProfileRepository.get_by_user_id(user_id)
