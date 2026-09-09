from app.industry.repositories.profile_repository import IndustryProfileRepository
from app.industry.models.industry import IndustryProfile
from app.industry.schemas.profile_schema import IndustryProfileUpdate
from fastapi import HTTPException, status

class IndustryProfileService:
    
    @staticmethod
    async def get_or_create_profile(user_id: str, company_name: str) -> IndustryProfile:
        profile = await IndustryProfileRepository.get_by_user_id(user_id)
        if not profile:
            new_profile = IndustryProfile(user_id=user_id, company_name=company_name)
            await IndustryProfileRepository.create_profile(new_profile)
            profile = await IndustryProfileRepository.get_by_user_id(user_id)
        return profile
        
    @staticmethod
    async def update_profile(user_id: str, data: IndustryProfileUpdate) -> IndustryProfile:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided to update")
            
        profile = await IndustryProfileRepository.update_profile(user_id, update_data)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile
