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

from app.core.constants import Approval, Roles
from app.auth.schemas.verify import VerifyEmailResponse
from fastapi import HTTPException, status


from app.student.models.student import Student
from app.student.repository.student_repository import StudentRepository

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

class AuthService:

    async def student_login(self, request: LoginRequest) -> TokenResponse:

        user = await DummySSOService.login(
            request.registration_no,
            request.password
        )


    # -----------------------------------------
    # 2. Create/update student profile
    # -----------------------------------------

        existing_student = await StudentRepository.find_by_registration_no(
            user["registration_no"]
        )

        if not existing_student:

            student = Student(
                registration_no=user["registration_no"],
                name=user["name"],
                email=user["email"]
            )

            await StudentRepository.create_student(student)

        access_token = create_access_token(
            {
                "sub": user["registration_no"],
                "role": user["role"]
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": user["registration_no"]
            }
        )

        await RedisService.save_refresh_token(
            user["registration_no"],
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

        # 4. Make sure only allowed non-student roles (admins use the admin portal)
        if user.role not in [
            Roles.ALUMNI,
            Roles.INDUSTRY
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This login method is not available for this role"
            )

        # 4b. Self-registered accounts need an admin's approval first
        self._ensure_approved(user)

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
            is_verified=False,
            approval_status=Approval.PENDING if request.role in Approval.ROLES else None
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

    async def verify_email(self,request: VerifyOTPRequest) -> VerifyEmailResponse:

        user = await UserRepository.find_by_email(
            request.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if user.is_verified:
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

        # Self-registered roles wait for an admin before they can sign in
        if user.role in Approval.ROLES and user.approval_status != Approval.APPROVED:

            from app.admin.services.notification_service import AdminNotificationService

            await AdminNotificationService.notify(
                title="New registration request",
                message=f"{user.email} wants to join as {user.role}.",
                type="registration",
                related_entity_id=user.id
            )

            return VerifyEmailResponse(
                message="Your email is verified. An admin will review your account and email you once you can sign in.",
                approval_status=Approval.PENDING
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

        return VerifyEmailResponse(
            message="Email verified",
            approval_status=user.approval_status,
            access_token=access_token,
            refresh_token=refresh_token,
            role=user.role
        )

    @staticmethod
    def _ensure_approved(user):

        if user.role not in Approval.ROLES or user.approval_status in (None, Approval.APPROVED):
            return

        if user.approval_status == Approval.REJECTED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your registration was not approved. Please contact the university for details."
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is awaiting admin approval. We'll email you as soon as you can sign in."
        )

    async def admin_login(self, request: UserLoginRequest) -> TokenResponse:

        user = await UserRepository.find_by_email(request.email)

        if not user or user.role != Roles.ADMIN or not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin email or password"
            )

        access_token = create_access_token({"sub": user.id, "role": user.role})
        refresh_token = create_refresh_token({"sub": user.id, "role": user.role})
        await RedisService.save_refresh_token(user.id, refresh_token)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=user.role
        )

    async def refresh_token(self,refresh_token: str) -> TokenResponse:

        # -----------------------------------------
        # 1. Decode refresh token
        # -----------------------------------------

        try:
            payload = decode_token(refresh_token)

        except Exception:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        # -----------------------------------------
        # 2. Get student identity
        # -----------------------------------------

        registration_no = payload.get("sub")

        if not registration_no:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # -----------------------------------------
        # 3. Check refresh token in Redis
        # -----------------------------------------

        stored_token = await RedisService.get_refresh_token(
            registration_no
        )

        if not stored_token:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found"
            )

        # -----------------------------------------
        # 4. Compare tokens
        # -----------------------------------------

        if stored_token != refresh_token:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # -----------------------------------------
        # 5. Create NEW access token
        # -----------------------------------------

        role = payload.get("role") or Roles.STUDENT

        access_token = create_access_token(
            {
                "sub": registration_no,
                "role": role
            }
        )

        # -----------------------------------------
        # 6. Return new access token
        # -----------------------------------------

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=role
        )