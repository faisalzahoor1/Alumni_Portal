from fastapi import APIRouter, Depends, UploadFile, File
from app.auth.models.user import User
from app.alumni.dependecies import get_current_alumni_user
from app.alumni.schemas.profile_schema import AlumniProfileUpdate, AlumniProfileResponse
from app.alumni.services.profile_service import AlumniProfileService

router = APIRouter(prefix="/profile", tags=["Alumni Profile"])


@router.get("/", response_model=AlumniProfileResponse)
async def get_profile(current_user: User = Depends(get_current_alumni_user)):
    profile = await AlumniProfileService.get_or_create_profile(
        user_id=current_user.id,
        email=current_user.email
    )
    return profile


@router.put("/", response_model=AlumniProfileResponse)
async def update_profile(
    data: AlumniProfileUpdate,
    current_user: User = Depends(get_current_alumni_user)
):
    profile = await AlumniProfileService.update_profile(
        user_id=current_user.id,
        data=data
    )
    return profile


@router.post("/avatar", response_model=AlumniProfileResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_alumni_user)
):
    profile = await AlumniProfileService.upload_avatar(
        user_id=current_user.id,
        file=file
    )
    return profile
