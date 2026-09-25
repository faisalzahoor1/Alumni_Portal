from datetime import datetime, timezone
from typing import Optional, List
import cloudinary.uploader
from fastapi import HTTPException, UploadFile, status
from app.database import cloudinary_config
from app.industry.models.post import Post
from app.industry.repositories.post_repository import PostRepository
from app.industry.schemas.post_schema import (
    PostCreate,
    PostUpdate,
    PostResponse,
)


class IndustryPostService:

    @staticmethod
    async def create_post(
        user_id: str,
        company_name: str,
        logo_url: Optional[str],
        data: PostCreate
    ) -> PostResponse:
        now = datetime.now(timezone.utc)
        post = Post(
            author_id=user_id,
            author_name=company_name,
            author_role="industry",
            author_avatar=logo_url,
            title=data.title,
            content=data.content,
            media_urls=data.media_urls or [],
            job_apply_url=data.job_apply_url,
            external_urls=data.external_urls or [],
            company_name=company_name,
            job_title=data.job_title,
            post_type=data.post_type or "job_opportunity",
            tags=data.tags or [],
            likes_count=0,
            comments_count=0,
            is_public=data.is_public if data.is_public is not None else True,
            created_at=now,
            updated_at=now
        )
        created_post = await PostRepository.create_post(post)
        return PostResponse(**created_post.model_dump())

    @staticmethod
    async def get_my_posts(user_id: str, limit: int = 50, skip: int = 0) -> List[PostResponse]:
        """Fetch posts created specifically by this industry user (only shown to him)."""
        posts = await PostRepository.get_by_author(author_id=user_id, limit=limit, skip=skip)
        return [PostResponse(**p.model_dump()) for p in posts]

    @staticmethod
    async def get_post_by_id(post_id: str, user_id: str) -> PostResponse:
        post = await PostRepository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        if post.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this post"
            )
        return PostResponse(**post.model_dump())

    @staticmethod
    async def update_post(post_id: str, user_id: str, data: PostUpdate) -> PostResponse:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided to update"
            )

        updated = await PostRepository.update_post(post_id, user_id, update_data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or unauthorized to update"
            )
        return PostResponse(**updated.model_dump())

    @staticmethod
    async def delete_post(post_id: str, user_id: str) -> bool:
        deleted = await PostRepository.delete_post(post_id, user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or unauthorized to delete"
            )
        return True

    @staticmethod
    async def upload_media(file: UploadFile) -> str:
        if file.content_type and not (
            file.content_type.startswith("image/") or
            file.content_type in ["application/pdf", "image/jpeg", "image/png", "image/webp", "image/gif"]
        ):
            raise HTTPException(status_code=400, detail="Only image and document files are supported")

        try:
            result = cloudinary.uploader.upload(
                file.file,
                resource_type="auto",
                folder="alumni_portal/industry_posts"
            )
            return result.get("secure_url") or result.get("url")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload media: {str(e)}"
            )
