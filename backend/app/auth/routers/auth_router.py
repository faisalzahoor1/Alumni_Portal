from fastapi import APIRouter

from app.auth.schemas.login import LoginRequest
from app.auth.schemas.token import TokenResponse
from app.auth.schemas.signup import SignupRequest, SignupResponse
from app.auth.schemas.otp import VerifyOTPRequest
from app.auth.services.auth_services import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

auth_service = AuthService()


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    return await auth_service.student_login(request)


@router.post("/signup",response_model=SignupResponse)
async def signup(request: SignupRequest):
    return await auth_service.signup(request)


@router.post("/verify-email",response_model=TokenResponse)
async def verify_email(request: VerifyOTPRequest):
    return await auth_service.verify_email(request)