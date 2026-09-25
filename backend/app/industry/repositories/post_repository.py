from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
import pymongo
from app.database import mongodb
from app.database.collections import Collections
from app.industry.models.post import Post


class PostRepository:

    @staticmethod
    async def create_post(post: Post) -> Post:
        post_dict = post.model_dump()
        result = await mongodb.database[Collections.POSTS].insert_one(post_dict)
        post.id = str(result.inserted_id)
        return post

    @staticmethod
    async def get_by_id(post_id: str) -> Optional[Post]:
        if not ObjectId.is_valid(post_id):
            return None
        document = await mongodb.database[Collections.POSTS].find_one({"_id": ObjectId(post_id)})
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        return Post(**document)

    @staticmethod
    async def get_by_author(author_id: str, limit: int = 50, skip: int = 0) -> List[Post]:
        cursor = (
            mongodb.database[Collections.POSTS]
            .find({"author_id": author_id})
            .sort("created_at", pymongo.DESCENDING)
            .skip(skip)
            .limit(limit)
        )
        posts = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            posts.append(Post(**doc))
        return posts

    @staticmethod
    async def count_by_author(author_id: str) -> int:
        return await mongodb.database[Collections.POSTS].count_documents({"author_id": author_id})

    @staticmethod
    async def update_post(post_id: str, author_id: str, update_data: dict) -> Optional[Post]:
        if not ObjectId.is_valid(post_id):
            return None
        update_data["updated_at"] = datetime.now(timezone.utc)
        result = await mongodb.database[Collections.POSTS].update_one(
            {"_id": ObjectId(post_id), "author_id": author_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            return None
        return await PostRepository.get_by_id(post_id)

    @staticmethod
    async def delete_post(post_id: str, author_id: str) -> bool:
        if not ObjectId.is_valid(post_id):
            return False
        result = await mongodb.database[Collections.POSTS].delete_one({
            "_id": ObjectId(post_id),
            "author_id": author_id
        })
        return result.deleted_count > 0
