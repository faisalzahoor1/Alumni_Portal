from typing import List, Optional
from fastapi import APIRouter, Depends, File, Query, UploadFile
from app.auth.models.user import User
from app.core.constants import Approval, Reports, Roles
from app.admin.dependencies import get_current_admin
from app.admin.schemas.admin_schema import (
    AdminDashboardStats,
    AdminNotificationResponse,
    AdminProfileResponse,
    AdminProfileUpdate,
    ManagedUserPage,
    RegistrationDecisionResponse,
    RegistrationResponse,
    ReportedPost,
    UnreadCountResponse,
)
from app.admin.services.dashboard_service import AdminDashboardService
from app.admin.services.notification_service import AdminNotificationService
from app.admin.services.profile_service import AdminProfileService
from app.admin.services.registration_service import RegistrationService
from app.admin.services.report_service import ReportService
from app.admin.services.university_post_service import UniversityPostService
from app.admin.services.user_management_service import UserManagementService
from app.alumni.schemas.post_schema import MediaUploadResponse, PostCreate, PostResponse, PostUpdate

# Every route here requires an admin
router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_admin)])


# ---------- Dashboard ----------

@router.get("/dashboard/stats", response_model=AdminDashboardStats)
async def get_stats():
    return await AdminDashboardService.get_stats()


# ---------- Registrations ----------

@router.get("/registrations", response_model=List[RegistrationResponse])
async def list_registrations(status: str = Query(Approval.PENDING)):
    """Verified alumni/industry sign-ups by approval status."""
    return await RegistrationService.list(status)


@router.post("/registrations/{user_id}/approve", response_model=RegistrationDecisionResponse)
async def approve_registration(user_id: str):
    return await RegistrationService.decide(user_id, approve=True)


@router.post("/registrations/{user_id}/reject", response_model=RegistrationDecisionResponse)
async def reject_registration(user_id: str):
    return await RegistrationService.decide(user_id, approve=False)


# ---------- Users ----------

@router.get("/users", response_model=ManagedUserPage)
async def search_users(
    role: str = Query(Roles.STUDENT),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1)
):
    return await UserManagementService.search(role, search, page)


@router.delete("/users/{role}/{user_id}")
async def delete_user(role: str, user_id: str):
    """Delete a student, alumni or industry account with everything it owns."""
    return await UserManagementService.delete(role, user_id)


# ---------- University posts ----------

@router.get("/posts", response_model=List[PostResponse])
async def list_university_posts(limit: int = Query(50, ge=1, le=100), skip: int = Query(0, ge=0)):
    return await UniversityPostService.list(limit, skip)


@router.post("/posts", response_model=PostResponse)
async def create_university_post(data: PostCreate, admin: User = Depends(get_current_admin)):
    return await UniversityPostService.create(admin, data)


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_university_post(post_id: str, data: PostUpdate):
    return await UniversityPostService.update(post_id, data)


@router.delete("/posts/{post_id}")
async def delete_university_post(post_id: str):
    return await UniversityPostService.delete(post_id)


@router.post("/posts/upload-media", response_model=MediaUploadResponse)
async def upload_university_post_media(file: UploadFile = File(...)):
    return await UniversityPostService.upload_media(file)


# ---------- Reports ----------

@router.get("/reports", response_model=List[ReportedPost])
async def list_reports(status: str = Query(Reports.PENDING)):
    """Reported posts grouped by post, most-reported first."""
    return await ReportService.list(status)


@router.post("/reports/{post_id}/dismiss")
async def allow_reported_post(post_id: str):
    """Keep the post and close its open reports."""
    return await ReportService.dismiss(post_id)


@router.delete("/reports/{post_id}/post")
async def delete_reported_post(post_id: str):
    """Delete the reported post (with its comments and reactions) and close its reports."""
    return await ReportService.remove_post(post_id)


# ---------- Notifications ----------

@router.get("/notifications", response_model=List[AdminNotificationResponse])
async def list_notifications(
    unread_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0)
):
    return await AdminNotificationService.list(unread_only, limit, skip)


@router.get("/notifications/unread-count", response_model=UnreadCountResponse)
async def unread_count():
    return UnreadCountResponse(unread_count=await AdminNotificationService.unread_count())


@router.put("/notifications/read-all")
async def mark_all_read():
    return await AdminNotificationService.mark_all_read()


@router.put("/notifications/{notification_id}/read")
async def mark_read(notification_id: str):
    return await AdminNotificationService.mark_read(notification_id)


@router.delete("/notifications/{notification_id}")
async def delete_notification(notification_id: str):
    return await AdminNotificationService.delete(notification_id)


# ---------- Profile ----------

@router.get("/profile", response_model=AdminProfileResponse)
async def get_profile(admin: User = Depends(get_current_admin)):
    return await AdminProfileService.get(admin)


@router.put("/profile", response_model=AdminProfileResponse)
async def update_profile(data: AdminProfileUpdate, admin: User = Depends(get_current_admin)):
    return await AdminProfileService.update(admin, data.name)


@router.post("/profile/avatar", response_model=AdminProfileResponse)
async def upload_avatar(file: UploadFile = File(...), admin: User = Depends(get_current_admin)):
    return await AdminProfileService.upload_avatar(admin, file)
