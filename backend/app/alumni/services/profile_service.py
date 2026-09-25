from typing import Optional
from fastapi import HTTPException, UploadFile, status
from app.alumni.repositories.profile_repository import AlumniProfileRepository
from app.alumni.models.alumni import AlumniProfile
from app.alumni.schemas.profile_schema import AlumniProfileUpdate
from app.alumni.services.media_service import MediaService


class AlumniProfileService:

    @staticmethod
    async def get_or_create_profile(
        user_id: str,
        email: str,
        default_name: Optional[str] = None
    ) -> AlumniProfile:
        profile = await AlumniProfileRepository.get_by_user_id(user_id)
        if not profile:
            name = default_name or email.split("@")[0].capitalize()
            new_profile = AlumniProfile(
                user_id=user_id,
                name=name,
                email=email
            )
            await AlumniProfileRepository.create_profile(new_profile)
            profile = await AlumniProfileRepository.get_by_user_id(user_id)
        return profile

    @staticmethod
    async def update_profile(user_id: str, data: AlumniProfileUpdate) -> AlumniProfile:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided to update"
            )

        profile = await AlumniProfileRepository.update_profile(user_id, update_data)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        return profile

    @staticmethod
    async def upload_avatar(user_id: str, file: UploadFile) -> AlumniProfile:
        avatar_url = await MediaService.upload_image(file, folder="alumni_portal/avatars")
        profile = await AlumniProfileRepository.update_profile(user_id, {"avatar_url": avatar_url})
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        return profile
