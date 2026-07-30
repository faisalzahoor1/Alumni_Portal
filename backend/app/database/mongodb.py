# app/database/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings

client: AsyncIOMotorClient | None = None
database: AsyncIOMotorDatabase | None = None


async def connect_to_mongodb():

    global client
    global database

    client = AsyncIOMotorClient(settings.MONGODB_URL)

    database = client[settings.DATABASE_NAME]


async def close_mongodb():

    global client

    if client:
        client.close()