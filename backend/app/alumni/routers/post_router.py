from typing import List
from fastapi import APIRouter, Depends, Query, UploadFile, File
from app.auth.models.user import User
from app.alumni.dependecies import get_current_alumni_user
from app.alumni.schemas.post_schema import (
    PostCreate,
    PostUpdate,
    PostResponse,
    MediaUploadResponse,
)
from app.alumni.services.post_service import PostService
from app.alumni.services.profile_service import AlumniProfileService

router = APIRouter(prefix="/posts", tags=["Alumni Posts"])


@router.post("/", response_model=PostResponse)
async def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_alumni_user)
):
    profile = await AlumniProfileService.get_or_create_profile(
        user_id=current_user.id,
        email=current_user.email
    )
    author_name = profile.name if profile and profile.name else current_user.email
    author_avatar = profile.avatar_url if profile else None

    return await PostService.create_post(
        user_id=current_user.id,
        user_role=current_user.role,
        author_name=author_name,
        author_avatar=author_avatar,
        data=data
    )


@router.get("/", response_model=List[PostResponse])
async def get_my_posts(
    limit: int = Query(50, ge=1, le=100, description="Max posts to return"),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: User = Depends(get_current_alumni_user)
):
    """Retrieve only the posts created by the current alumni."""
    return await PostService.get_my_posts(
        user_id=current_user.id,
        limit=limit,
        skip=skip
    )


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: User = Depends(get_current_alumni_user)
):
    return await PostService.get_post_by_id(
        post_id=post_id,
        user_id=current_user.id
    )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    data: PostUpdate,
    current_user: User = Depends(get_current_alumni_user)
):
    return await PostService.update_post(
        post_id=post_id,
        user_id=current_user.id,
        data=data
    )


@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_alumni_user)
):
    await PostService.delete_post(
        post_id=post_id,
        user_id=current_user.id
    )
    return {"message": "Post deleted successfully"}


@router.post("/upload-media", response_model=MediaUploadResponse)
async def upload_post_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_alumni_user)
):
    """Upload picture of achievements, documents or media to Cloudinary."""
    file_url = await PostService.upload_post_media(file)
    return MediaUploadResponse(
        file_url=file_url,
        file_name=file.filename
    )
