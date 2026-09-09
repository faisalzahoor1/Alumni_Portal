from fastapi import FastAPI

from app.core.config import settings
from app.core.lifespan import lifespan

from app.middlewares.cors import configure_cors
from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.auth_middleware import RequestIDMiddleware

from app.auth.routers.auth_router import router as auth_router
from app.student.routers.profile_router import router as student_profile_router


from app.auth.routers.auth_router import router as auth_router
from app.industry.routers.profile_router import router as industry_profile_router
from app.industry.routers.job_router import router as industry_job_router
from app.industry.routers.dashboard_router import router as industry_dashboard_router
from app.industry.routers.notification_router import router as industry_notification_router

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

@app.get("/")
async def root():

    return {
        "status": "running"
    }