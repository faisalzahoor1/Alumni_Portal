import random

from app.database import redis
from app.core.constants import OTP, RedisKeys


class OTPService:

    @staticmethod
    def generate_otp() -> str:
        """
        Generate a random numeric OTP.
        """

        return "".join(
            random.choices("0123456789", k=OTP.LENGTH)
        )

    @staticmethod
    async def save_otp(email: str, otp: str):

        key = f"{RedisKeys.OTP}:{email}"

        await redis.redis_client.set(
            key,
            otp,
            ex=OTP.EXPIRY_SECONDS
        )

    @staticmethod
    async def get_otp(email: str):

        key = f"{RedisKeys.OTP}:{email}"

        return await redis.redis_client.get(key)

    @staticmethod
    async def delete_otp(email: str):

        key = f"{RedisKeys.OTP}:{email}"

        await redis.redis_client.delete(key)

    @staticmethod
    async def verify_otp(email: str, entered_otp: str) -> bool:

        stored_otp = await OTPService.get_otp(email)

        if stored_otp is None:
            return False

        if stored_otp != entered_otp:
            return False

        await OTPService.delete_otp(email)

        return True