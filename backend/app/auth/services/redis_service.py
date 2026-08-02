from app.database import redis


class RedisService:

    @staticmethod
    async def save_refresh_token(user_id,token):

        await redis.redis_client.set(f"refresh:{user_id}",token)

    @staticmethod
    async def get_refresh_token(user_id):

        return await redis.redis_client.get(f"refresh:{user_id}")

    @staticmethod
    async def delete_refresh_token(user_id):

        await redis.redis_client.delete(f"refresh:{user_id}")