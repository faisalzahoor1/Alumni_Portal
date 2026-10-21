from typing import List
from fastapi import HTTPException, UploadFile, status
from app.auth.models.user import User
from app.core.constants import Reports, University
from app.alumni.models.post import Post
from app.alumni.schemas.post_schema import PostCreate, PostResponse, PostUpdate
from app.alumni.services.media_service import MediaService
from app.admin.repositories.post_repository import AdminPostRepository
from app.admin.repositories.report_repository import ReportRepository
from app.admin.services.profile_service import AdminProfileService


class UniversityPostService:
    """Official posts by admins, published under the university's name."""

    @staticmethod
    async def list(limit: int, skip: int) -> List[PostResponse]:
        posts = await AdminPostRepository.list_by_role(University.AUTHOR_ROLE, limit, skip)
        return [PostResponse(**p.model_dump()) for p in posts]

    @staticmethod
    async def create(admin: User, data: PostCreate) -> PostResponse:
        profile = await AdminProfileService.get_or_create(admin)
        post = await AdminPostRepository.create(Post(
            author_id=admin.id,
            author_name=University.NAME,
            author_role=University.AUTHOR_ROLE,
            author_avatar=profile.avatar_url,
            **data.model_dump(exclude_none=True)
        ))
        return PostResponse(**post.model_dump())

    @staticmethod
    async def update(post_id: str, data: PostUpdate) -> PostResponse:
        post = await AdminPostRepository.update(post_id, University.AUTHOR_ROLE, data.model_dump(exclude_unset=True))
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="University post not found")
        return PostResponse(**post.model_dump())

    @staticmethod
    async def delete(post_id: str) -> dict:
        post = await AdminPostRepository.get(post_id)
        if not post or post.author_role != University.AUTHOR_ROLE:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="University post not found")
        await AdminPostRepository.delete_with_engagement(post_id)
        await ReportRepository.resolve_for_post(post_id, Reports.ACTIONED)
        return {"message": "Post deleted"}

    @staticmethod
    async def upload_media(file: UploadFile) -> dict:
        url = await MediaService.upload_image(file, folder="alumni_portal/university_posts")
        return {"file_url": url}
