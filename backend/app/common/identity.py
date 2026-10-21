# app/common/identity.py

from app.core.constants import Roles


async def get_display_identity(entity: dict) -> dict:
    """
    Public name and avatar for a signed-in entity.
    Alumni use their profile name/photo and industry their company name/logo;
    students already carry their SSO name.
    """
    name, avatar_url = entity["name"], entity.get("avatar_url")

    if entity["role"] == Roles.ALUMNI:
        from app.alumni.repositories.profile_repository import AlumniProfileRepository
        profile = await AlumniProfileRepository.get_by_user_id(entity["id"])
        if profile:
            name, avatar_url = profile.name or name, profile.avatar_url

    elif entity["role"] == Roles.ADMIN:
        from app.admin.repositories.profile_repository import AdminProfileRepository
        profile = await AdminProfileRepository.get_by_user_id(entity["id"])
        if profile:
            name, avatar_url = profile.name or name, profile.avatar_url

    elif entity["role"] == Roles.INDUSTRY:
        from app.industry.repositories.profile_repository import IndustryProfileRepository
        profile = await IndustryProfileRepository.get_by_user_id(entity["id"])
        if profile:
            name, avatar_url = profile.company_name or name, profile.logo_url

    return {"name": name, "avatar_url": avatar_url}
