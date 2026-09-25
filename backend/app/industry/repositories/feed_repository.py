from typing import List, Optional
from bson import ObjectId
import pymongo
from app.database import mongodb
from app.database.collections import Collections
from app.industry.models.post import Post


class IndustryFeedRepository:

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
    async def get_feed(
        roles: Optional[List[str]] = None,
        post_type: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 20,
        skip: int = 0
    ) -> List[Post]:
        """Fetch posts from both alumni and industry for the feed."""
        query = {"is_public": True}
        if roles:
            query["author_role"] = {"$in": roles}
        if post_type:
            query["post_type"] = post_type
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"tags": {"$in": [search]}},
                {"company_name": {"$regex": search, "$options": "i"}}
            ]

        cursor = (
            mongodb.database[Collections.POSTS]
            .find(query)
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
    async def count_feed(
        roles: Optional[List[str]] = None,
        post_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> int:
        """Count total public posts for the feed."""
        query = {"is_public": True}
        if roles:
            query["author_role"] = {"$in": roles}
        if post_type:
            query["post_type"] = post_type
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"tags": {"$in": [search]}},
                {"company_name": {"$regex": search, "$options": "i"}}
            ]
        return await mongodb.database[Collections.POSTS].count_documents(query)
