from fastapi import FastAPI

from app.core.config import settings
from app.core.lifespan import lifespan

from app.middlewares.cors import configure_cors
from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.auth_middleware import RequestIDMiddleware

from app.auth.routers.auth_router import router as auth_router
from app.student.routers.profile_router import router as student_profile_router

from app.industry.routers.profile_router import router as industry_profile_router
from app.industry.routers.job_router import router as industry_job_router
from app.industry.routers.dashboard_router import router as industry_dashboard_router
from app.industry.routers.notification_router import router as industry_notification_router
from app.industry.routers.feed_router import router as industry_feed_router

from app.alumni.routers.profile_router import router as alumni_profile_router
from app.alumni.routers.post_router import router as alumni_post_router
from app.alumni.routers.dashboard_router import router as alumni_dashboard_router
from app.alumni.routers.notification_router import router as alumni_notification_router
from app.alumni.routers.feed_router import router as alumni_feed_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

configure_cors(app)

app.add_middleware(RequestIDMiddleware)

app.add_middleware(LoggingMiddleware)


app.include_router(
    auth_router,
    prefix=settings.API_PREFIX
)

#Student Routers
app.include_router(
    student_profile_router,
    prefix=settings.API_PREFIX
)

# Industry Routers
app.include_router(
    industry_profile_router,
    prefix=f"{settings.API_PREFIX}/industry"
)
app.include_router(
    industry_job_router,
    prefix=f"{settings.API_PREFIX}/industry"
)
app.include_router(
    industry_dashboard_router,
    prefix=f"{settings.API_PREFIX}/industry"
)
app.include_router(
    industry_notification_router,
    prefix=f"{settings.API_PREFIX}/industry"
)
app.include_router(
    industry_feed_router,
    prefix=f"{settings.API_PREFIX}/industry"
)

# Alumni Routers
app.include_router(
    alumni_profile_router,
    prefix=f"{settings.API_PREFIX}/alumni"
)
app.include_router(
    alumni_post_router,
    prefix=f"{settings.API_PREFIX}/alumni"
)
app.include_router(
    alumni_dashboard_router,
    prefix=f"{settings.API_PREFIX}/alumni"
)
app.include_router(
    alumni_notification_router,
    prefix=f"{settings.API_PREFIX}/alumni"
)
app.include_router(
    alumni_feed_router,
    prefix=f"{settings.API_PREFIX}/alumni"
)

# Shared Community Feed (also available directly at /api/feed for all users)
app.include_router(
    alumni_feed_router,
    prefix=settings.API_PREFIX
)


@app.get("/")
async def root():

    return {
        "status": "running"
    }