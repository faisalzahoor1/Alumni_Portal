from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

from app.core.constants import Reports
from app.alumni.schemas.post_schema import PostResponse


# ---------- Notifications ----------

class AdminNotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    type: str
    related_entity_id: Optional[str] = None
    is_read: bool
    created_at: datetime


class UnreadCountResponse(BaseModel):
    unread_count: int


# ---------- Registrations ----------

class RegistrationResponse(BaseModel):
    id: str
    email: str
    role: str
    name: Optional[str] = None
    approval_status: str
    created_at: Optional[datetime] = None


class RegistrationDecisionResponse(BaseModel):
    registration: RegistrationResponse
    email_sent: bool


# ---------- Users ----------

class ManagedUser(BaseModel):
    id: str
    role: str
    name: str
    email: str
    registration_no: Optional[str] = None
    avatar_url: Optional[str] = None
    approval_status: Optional[str] = None
    created_at: Optional[datetime] = None


class ManagedUserPage(BaseModel):
    users: List[ManagedUser]
    total: int
    page: int
    limit: int
    has_more: bool


# ---------- Reports ----------

class ReportCreate(BaseModel):
    reason: str
    details: Optional[str] = Field(None, max_length=Reports.DETAILS_MAX_LENGTH)

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, reason: str):
        allowed = [r["value"] for r in Reports.REASONS]
        if reason not in allowed:
            raise ValueError(f"Reason must be one of: {', '.join(allowed)}")
        return reason


class ReportItem(BaseModel):
    id: str
    reporter_id: str
    reporter_role: str
    reporter_name: str
    reason: str
    details: Optional[str] = None
    status: str
    created_at: datetime


class ReportedPost(BaseModel):
    post_id: str
    post: Optional[PostResponse] = None  # None if the post no longer exists
    report_count: int
    reasons: Dict[str, int]
    last_reported_at: datetime
    reports: List[ReportItem]


# ---------- Profile & dashboard ----------

class AdminProfileResponse(BaseModel):
    id: str
    user_id: str
    name: str
    email: str
    avatar_url: Optional[str] = None


class AdminProfileUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class AdminDashboardStats(BaseModel):
    pending_registrations: int
    open_reports: int
    reported_posts: int
    students: int
    alumni: int
    industry: int
    university_posts: int
    community_posts: int
    unread_notifications: int
