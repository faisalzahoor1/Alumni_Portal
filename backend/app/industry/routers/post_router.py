from typing import List
from fastapi import APIRouter, Depends, Query, UploadFile, File
from app.auth.models.user import User
from app.industry.dependecies import get_current_industry_user
from app.industry.schemas.post_schema import (
    PostCreate,
    PostUpdate,
    PostResponse,
    MediaUploadResponse,
)
from app.industry.services.post_service import IndustryPostService
from app.industry.services.profile_service import IndustryProfileService

router = APIRouter(prefix="/posts", tags=["Industry Posts"])


@router.post("/", response_model=PostResponse)
async def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_industry_user)
):
    """Create a post as an Industry organization (job announcements, hiring drives, form links, etc.)."""
    company_name = getattr(current_user, "company_name", None) or getattr(current_user, "companyName", None) or current_user.email
    profile = await IndustryProfileService.get_or_create_profile(current_user.id, company_name)
    author_name = profile.company_name if profile and profile.company_name else company_name
    author_logo = profile.logo_url if profile else None

    return await IndustryPostService.create_post(
        user_id=current_user.id,
        company_name=author_name,
        logo_url=author_logo,
        data=data
    )


@router.get("/", response_model=List[PostResponse])
async def get_my_posts(
    limit: int = Query(50, ge=1, le=100, description="Max posts to return"),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: User = Depends(get_current_industry_user)
):
    """Retrieve only the posts created by this industry organization (shown only to him)."""
    return await IndustryPostService.get_my_posts(
        user_id=current_user.id,
        limit=limit,
        skip=skip
    )


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: User = Depends(get_current_industry_user)
):
    """Retrieve a single post created by this industry organization."""
    return await IndustryPostService.get_post_by_id(
        post_id=post_id,
        user_id=current_user.id
    )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    data: PostUpdate,
    current_user: User = Depends(get_current_industry_user)
):
    """Update a post created by this industry organization."""
    return await IndustryPostService.update_post(
        post_id=post_id,
        user_id=current_user.id,
        data=data
    )


@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_industry_user)
):
    """Delete a post created by this industry organization."""
    await IndustryPostService.delete_post(
        post_id=post_id,
        user_id=current_user.id
    )
    return {"message": "Post deleted successfully"}


@router.post("/upload-media", response_model=MediaUploadResponse)
async def upload_post_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_industry_user)
):
    """Upload picture/banner or media for an industry post to Cloudinary."""
    file_url = await IndustryPostService.upload_media(file)
    return MediaUploadResponse(
        file_url=file_url,
        file_name=file.filename
    )
