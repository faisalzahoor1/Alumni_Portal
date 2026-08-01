from app.database import redis


class RedisService:

    @staticmethod
    async def save_refresh_token(

        student_id,

        token

    ):

        await redis.redis_client.set(

            f"refresh:{student_id}",

            token

        )

    @staticmethod
    async def get_refresh_token(

        student_id

    ):

        return await redis.redis_client.get(

            f"refresh:{student_id}"

        )

    @staticmethod
    async def delete_refresh_token(

        student_id

    ):

        await redis.redis_client.delete(

            f"refresh:{student_id}"

        )