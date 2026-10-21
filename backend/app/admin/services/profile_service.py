from fastapi import UploadFile
from app.auth.models.user import User
from app.common.avatar_service import AvatarService
from app.admin.models.admin_profile import AdminProfile
from app.admin.repositories.profile_repository import AdminProfileRepository
from app.admin.schemas.admin_schema import AdminProfileResponse


class AdminProfileService:

    @staticmethod
    async def get_or_create(user: User) -> AdminProfile:
        profile = await AdminProfileRepository.get_by_user_id(user.id)
        if not profile:
            profile = await AdminProfileRepository.create(
                AdminProfile(user_id=user.id, name=user.email.split("@")[0].replace(".", " ").title())
            )
        return profile

    @staticmethod
    def _response(profile: AdminProfile, user: User) -> AdminProfileResponse:
        return AdminProfileResponse(**profile.model_dump(include={"id", "user_id", "name", "avatar_url"}), email=user.email)

    @staticmethod
    async def get(user: User) -> AdminProfileResponse:
        return AdminProfileService._response(await AdminProfileService.get_or_create(user), user)

    @staticmethod
    async def update(user: User, name: str) -> AdminProfileResponse:
        await AdminProfileService.get_or_create(user)
        profile = await AdminProfileRepository.update(user.id, {"name": name.strip()})
        return AdminProfileService._response(profile, user)

    @staticmethod
    async def upload_avatar(user: User, file: UploadFile) -> AdminProfileResponse:
        await AdminProfileService.get_or_create(user)
        avatar_url = await AvatarService.upload(file, folder="alumni_portal/admin_avatars")
        profile = await AdminProfileRepository.update(user.id, {"avatar_url": avatar_url})
        await AvatarService.propagate(user.id, avatar_url)
        return AdminProfileService._response(profile, user)
