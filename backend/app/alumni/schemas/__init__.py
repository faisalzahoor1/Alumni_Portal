from app.alumni.schemas.profile_schema import AlumniProfileUpdate, AlumniProfileResponse
from app.alumni.schemas.post_schema import (
    PostCreate,
    PostUpdate,
    PostResponse,
    MediaUploadResponse,
)
from app.alumni.schemas.feed_schema import FeedResponse
from app.alumni.schemas.dashboard_schema import AlumniDashboardStats
from app.alumni.schemas.notification_schema import NotificationResponse, UnreadCountResponse

__all__ = [
    "AlumniProfileUpdate",
    "AlumniProfileResponse",
    "PostCreate",
    "PostUpdate",
    "PostResponse",
    "MediaUploadResponse",
    "FeedResponse",
    "AlumniDashboardStats",
    "NotificationResponse",
    "UnreadCountResponse",
]
