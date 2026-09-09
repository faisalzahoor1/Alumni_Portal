from typing import List
from fastapi import APIRouter, Depends, Query

from app.auth.models.user import User
from app.industry.dependecies import get_current_industry_user
from app.industry.schemas.notification_schema import (
    NotificationResponse,
    UnreadCountResponse,
)
from app.industry.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Industry Notifications"])


@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    unread_only: bool = Query(False, description="Filter for unread notifications only"),
    limit: int = Query(50, ge=1, le=100, description="Max notifications to return"),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: User = Depends(get_current_industry_user)
):
    return await NotificationService.get_notifications(
        recipient_id=current_user.id,
        unread_only=unread_only,
        limit=limit,
        skip=skip
    )


@router.get("/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(current_user: User = Depends(get_current_industry_user)):
    count = await NotificationService.get_unread_count(recipient_id=current_user.id)
    return UnreadCountResponse(unread_count=count)


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_industry_user)
):
    return await NotificationService.mark_as_read(
        notification_id=notification_id,
        recipient_id=current_user.id
    )


@router.put("/read-all")
async def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_industry_user)
):
    return await NotificationService.mark_all_as_read(recipient_id=current_user.id)


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_industry_user)
):
    return await NotificationService.delete_notification(
        notification_id=notification_id,
        recipient_id=current_user.id
    )
