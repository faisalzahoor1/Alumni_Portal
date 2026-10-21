from datetime import datetime, timezone
from typing import Dict, List, Optional
from bson import ObjectId
import pymongo
from app.database import mongodb
from app.database.collections import Collections
from app.engagement.models.comment import Comment


class EngagementRepository:

    @staticmethod
    async def get_public_post(post_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(post_id):
            return None
        return await mongodb.database[Collections.POSTS].find_one({"_id": ObjectId(post_id), "is_public": True})

    # ---------- Reactions ----------

    @staticmethod
    async def set_reaction(post_id: str, user_id: str, reaction: Optional[str]):
        collection = mongodb.database[Collections.REACTIONS]
        if reaction is None:
            await collection.delete_one({"post_id": post_id, "user_id": user_id})
            return
        await collection.update_one(
            {"post_id": post_id, "user_id": user_id},
            {"$set": {"reaction": reaction, "updated_at": datetime.now(timezone.utc)}},
            upsert=True
        )

    @staticmethod
    async def get_reactions_for_user(post_ids: List[str], user_id: str) -> Dict[str, str]:
        cursor = mongodb.database[Collections.REACTIONS].find({"post_id": {"$in": post_ids}, "user_id": user_id})
        return {doc["post_id"]: doc["reaction"] async for doc in cursor}

    @staticmethod
    async def refresh_counts(post_id: str, reactions: List[str]) -> dict:
        """Recount reactions and comments from source so counters never drift."""
        counts = {
            f"{reaction}s_count": await mongodb.database[Collections.REACTIONS].count_documents(
                {"post_id": post_id, "reaction": reaction}
            )
            for reaction in reactions
        }
        counts["comments_count"] = await mongodb.database[Collections.COMMENTS].count_documents({"post_id": post_id})
        await mongodb.database[Collections.POSTS].update_one({"_id": ObjectId(post_id)}, {"$set": counts})
        return counts

    # ---------- Comments ----------

    @staticmethod
    async def create_comment(comment: Comment) -> Comment:
        result = await mongodb.database[Collections.COMMENTS].insert_one(comment.model_dump(exclude={"id"}))
        comment.id = str(result.inserted_id)
        return comment

    @staticmethod
    async def get_comment(post_id: str, comment_id: str) -> Optional[Comment]:
        if not ObjectId.is_valid(comment_id):
            return None
        doc = await mongodb.database[Collections.COMMENTS].find_one({"_id": ObjectId(comment_id), "post_id": post_id})
        if not doc:
            return None
        doc["id"] = str(doc.pop("_id"))
        return Comment(**doc)

    @staticmethod
    async def get_comments(post_id: str, limit: int, skip: int) -> List[Comment]:
        cursor = (
            mongodb.database[Collections.COMMENTS]
            .find({"post_id": post_id})
            .sort("created_at", pymongo.ASCENDING)
            .skip(skip)
            .limit(limit)
        )
        comments = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            comments.append(Comment(**doc))
        return comments

    @staticmethod
    async def delete_comment(post_id: str, comment_id: str, author_id: str) -> bool:
        if not ObjectId.is_valid(comment_id):
            return False
        result = await mongodb.database[Collections.COMMENTS].delete_one(
            {"_id": ObjectId(comment_id), "post_id": post_id, "author_id": author_id}
        )
        if result.deleted_count == 0:
            return False
        # Replies go with their comment
        await mongodb.database[Collections.COMMENTS].delete_many({"post_id": post_id, "parent_id": comment_id})
        return True
