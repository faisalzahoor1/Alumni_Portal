from app.auth.repository.user_repository import UserRepository
from app.auth.models.user import User


from app.auth.schemas.login import LoginRequest, UserLoginRequest
from app.auth.schemas.token import TokenResponse
from app.auth.schemas.signup import SignupRequest, SignupResponse
from app.auth.schemas.otp import VerifyOTPRequest

from app.auth.services.email_service import EmailService
from app.auth.services.otp_service import OTPService
from app.auth.services.redis_service import RedisService
from app.auth.services.sso_service import DummySSOService

from app.core.constants import Roles
from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

class AuthService:

    async def student_login(self, request: LoginRequest) -> TokenResponse:

        user = await DummySSOService.login(
            request.registration_no,
            request.password
        )

        access_token = create_access_token(
            {
                "sub": user["user_id"],
                "role": user["role"]
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": user["user_id"]
            }
        )

        await RedisService.save_refresh_token(
            user["user_id"],
            refresh_token
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=user["role"]
        )


    async def user_login(self,request: UserLoginRequest) -> TokenResponse:

        # 1. Find user by email
        user = await UserRepository.find_by_email(
            request.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # 2. Check whether email is verified
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email first"
            )

        # 3. Verify password
        password_valid = verify_password(
            request.password,
            user.hashed_password
        )

        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # 4. Make sure only allowed non-student roles
        if user.role not in [
            Roles.ADMIN,
            Roles.ALUMNI,
            Roles.INDUSTRY
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This login method is not available for this role"
            )

        # 5. Create access token
        access_token = create_access_token(
            {
                "sub": user.id,
                "role": user.role
            }
        )

        # 6. Create refresh token
        refresh_token = create_refresh_token(
            {
                "sub": user.id,
                "role": user.role
            }
        )

        # 7. Save refresh token in Redis
        await RedisService.save_refresh_token(
            user.id,
            refresh_token
        )

        # 8. Return tokens
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=user.role
        )



    async def signup(self, request: SignupRequest) -> SignupResponse:

        existing_user = await UserRepository.find_by_email(request.email)

        # -------------------------------------------------
        # User already exists
        # -------------------------------------------------

        if existing_user:

            # Already verified
            if existing_user.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists"
                )

            otp = OTPService.generate_otp()

            await OTPService.save_otp(
                request.email,
                otp
            )

            await EmailService.send_otp(
                request.email,
                otp
            )

            return SignupResponse(
                message="A new OTP has been sent to your email."
            )

        # -------------------------------------------------
        # New User
        # -------------------------------------------------

        hashed_password = hash_password(request.password)

        user = User(
            email=request.email,
            hashed_password=hashed_password,
            role=request.role,
            is_verified=False
        )

        await UserRepository.create_user(user)

        otp = OTPService.generate_otp()

        await OTPService.save_otp(
            request.email,
            otp
        )

        await EmailService.send_otp(
            request.email,
            otp
        )

        return SignupResponse(
            message="OTP sent successfully"
        )

    from fastapi import HTTPException, status

    async def verify_email(self,request: VerifyOTPRequest) -> TokenResponse:

        user = await UserRepository.find_by_email(
            request.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if user.is_verified:
            print(user.model_dump())
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified"
            )

        valid = await OTPService.verify_otp(
            request.email,
            request.otp
        )

        if not valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP"
            )

        await UserRepository.verify_user(
            request.email
        )

        access_token = create_access_token(
            {
                "sub": user.id,
                "role": user.role
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": user.id,
                "role": user.role
            }
        )

        await RedisService.save_refresh_token(
            user.id,
            refresh_token
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=user.role
        )