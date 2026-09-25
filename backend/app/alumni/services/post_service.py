from typing import List, Optional
from fastapi import HTTPException, UploadFile, status
from app.alumni.repositories.post_repository import PostRepository
from app.alumni.repositories.profile_repository import AlumniProfileRepository
from app.alumni.models.post import Post
from app.alumni.schemas.post_schema import PostCreate, PostUpdate
from app.alumni.services.media_service import MediaService


class PostService:

    @staticmethod
    async def create_post(
        user_id: str,
        user_role: str,
        author_name: str,
        author_avatar: Optional[str],
        data: PostCreate
    ) -> Post:
        post = Post(
            author_id=user_id,
            author_name=author_name,
            author_role=user_role,
            author_avatar=author_avatar,
            title=data.title,
            content=data.content,
            media_urls=data.media_urls or [],
            job_apply_url=data.job_apply_url,
            external_urls=data.external_urls or [],
            company_name=data.company_name,
            job_title=data.job_title,
            post_type=data.post_type or "general",
            tags=data.tags or [],
            is_public=data.is_public if data.is_public is not None else True
        )
        return await PostRepository.create_post(post)

    @staticmethod
    async def get_my_posts(user_id: str, limit: int = 50, skip: int = 0) -> List[Post]:
        return await PostRepository.get_by_author(author_id=user_id, limit=limit, skip=skip)

    @staticmethod
    async def get_post_by_id(post_id: str, user_id: str) -> Post:
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
        return post

    @staticmethod
    async def update_post(post_id: str, user_id: str, data: PostUpdate) -> Post:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided to update"
            )

        updated_post = await PostRepository.update_post(post_id, user_id, update_data)
        if not updated_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or unauthorized to update"
            )
        return updated_post

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
    async def upload_post_media(file: UploadFile) -> str:
        return await MediaService.upload_image(file, folder="alumni_portal/posts")
