from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
import pymongo
from app.database import mongodb
from app.database.collections import Collections
from app.alumni.models.post import Post


class AdminPostRepository:
    """University posts (author_role = University.AUTHOR_ROLE) and post removal for moderation."""

    @staticmethod
    def _to_post(doc: dict) -> Post:
        doc["id"] = str(doc.pop("_id"))
        return Post(**doc)

    @staticmethod
    async def get(post_id: str) -> Optional[Post]:
        if not ObjectId.is_valid(post_id):
            return None
        doc = await mongodb.database[Collections.POSTS].find_one({"_id": ObjectId(post_id)})
        return AdminPostRepository._to_post(doc) if doc else None

    @staticmethod
    async def list_by_role(author_role: str, limit: int, skip: int) -> List[Post]:
        cursor = (
            mongodb.database[Collections.POSTS]
            .find({"author_role": author_role})
            .sort("created_at", pymongo.DESCENDING)
            .skip(skip)
            .limit(limit)
        )
        return [AdminPostRepository._to_post(doc) async for doc in cursor]

    @staticmethod
    async def create(post: Post) -> Post:
        result = await mongodb.database[Collections.POSTS].insert_one(post.model_dump(exclude={"id"}))
        post.id = str(result.inserted_id)
        return post

    @staticmethod
    async def update(post_id: str, author_role: str, data: dict) -> Optional[Post]:
        if not ObjectId.is_valid(post_id):
            return None
        data["updated_at"] = datetime.now(timezone.utc)
        result = await mongodb.database[Collections.POSTS].update_one(
            {"_id": ObjectId(post_id), "author_role": author_role}, {"$set": data}
        )
        return await AdminPostRepository.get(post_id) if result.matched_count else None

    @staticmethod
    async def delete_with_engagement(post_id: str) -> bool:
        """Remove a post with its comments, reactions and reports."""
        if not ObjectId.is_valid(post_id):
            return False
        db = mongodb.database
        result = await db[Collections.POSTS].delete_one({"_id": ObjectId(post_id)})
        await db[Collections.COMMENTS].delete_many({"post_id": post_id})
        await db[Collections.REACTIONS].delete_many({"post_id": post_id})
        return result.deleted_count > 0

    @staticmethod
    async def count_by_roles(roles: List[str]) -> int:
        return await mongodb.database[Collections.POSTS].count_documents({"author_role": {"$in": roles}})
