from app.auth.schemas.login import LoginRequest
from app.auth.schemas.token import TokenResponse

from app.auth.services.jwt_service import JWTService
from app.auth.services.redis_service import RedisService
from app.auth.services.sso_service import DummySSOService


class AuthService:

    async def login(
        self,
        request: LoginRequest
    ) -> TokenResponse:

        student = await DummySSOService.login(
            request.registration_no,
            request.password
        )

        access_token = JWTService.create_access_token(
            {
                "sub": student["student_id"],
                "role": student["role"]
            }
        )

        refresh_token = JWTService.create_refresh_token(
            {
                "sub": student["student_id"]
            }
        )

        await RedisService.save_refresh_token(
            student["student_id"],
            refresh_token
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=student["role"]
        )