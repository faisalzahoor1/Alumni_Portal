from fastapi import APIRouter, Depends
from app.auth.models.user import User
from app.auth.dependensies import get_current_industry_user
from app.industry.schemas.profile_schema import IndustryProfileUpdate, IndustryProfileResponse
from app.industry.services.profile_service import IndustryProfileService

router = APIRouter(prefix="/profile", tags=["Industry Profile"])

@router.get("/", response_model=IndustryProfileResponse)
async def get_profile(current_user: User = Depends(get_current_industry_user)):
    # company_name defaults to User's company_name/companyName or email fallback
    company_name = getattr(current_user, "company_name", None) or getattr(current_user, "companyName", None) or current_user.email
    profile = await IndustryProfileService.get_or_create_profile(current_user.id, company_name)
    return profile

@router.put("/", response_model=IndustryProfileResponse)
async def update_profile(data: IndustryProfileUpdate, current_user: User = Depends(get_current_industry_user)):
    profile = await IndustryProfileService.update_profile(current_user.id, data)
    return profile
