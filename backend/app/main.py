from fastapi import FastAPI

from app.core.config import settings
from app.core.lifespan import lifespan

from app.middlewares.cors import configure_cors
from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.auth_middleware import RequestIDMiddleware

from app.auth.routers.auth_router import router as auth_router
from app.student.routers.profile_router import router as student_profile_router


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

app.include_router(
    student_profile_router,
    prefix=settings.API_PREFIX
)

@app.get("/")
async def root():

    return {
        "status": "running"
    }