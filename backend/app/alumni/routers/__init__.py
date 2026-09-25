from app.alumni.routers.profile_router import router as profile_router
from app.alumni.routers.post_router import router as post_router
from app.alumni.routers.feed_router import router as feed_router
from app.alumni.routers.dashboard_router import router as dashboard_router
from app.alumni.routers.notification_router import router as notification_router

__all__ = [
    "profile_router",
    "post_router",
    "feed_router",
    "dashboard_router",
    "notification_router",
]
