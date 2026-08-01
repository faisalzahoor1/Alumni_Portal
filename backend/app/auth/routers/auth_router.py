from fastapi import APIRouter

from app.auth.schemas.login import LoginRequest
from app.auth.schemas.token import TokenResponse
from app.auth.services.auth_services import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

auth_service = AuthService()


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    request: LoginRequest
):
    return await auth_service.login(request)