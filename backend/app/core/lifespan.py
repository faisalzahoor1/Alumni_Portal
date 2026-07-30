# app/core/lifespan.py

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging import logger

from app.database.mongodb import connect_to_mongodb

from app.database.mongodb import close_mongodb

from app.database.redis import connect_to_redis

from app.database.redis import close_redis

from app.database.indexes import create_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting Application")

    await connect_to_mongodb()

    await connect_to_redis()

    await create_indexes()

    logger.info("Database Connected")

    logger.info("Redis Connected")

    yield

    logger.info("Closing Application")

    await close_mongodb()

    await close_redis()