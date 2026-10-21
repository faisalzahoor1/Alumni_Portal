from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
import pymongo
from app.database import mongodb
from app.database.collections import Collections


class MessageRepository:

    @staticmethod
    def _with_id(doc: Optional[dict]) -> Optional[dict]:
        if doc:
            doc["id"] = str(doc.pop("_id"))
        return doc

    # ---------- Conversations ----------

    @staticmethod
    async def find_conversation(initiator_id: str, recipient_id: str) -> Optional[dict]:
        doc = await mongodb.database[Collections.CONVERSATIONS].find_one(
            {"initiator.id": initiator_id, "recipient.id": recipient_id}
        )
        return MessageRepository._with_id(doc)

    @staticmethod
    async def create_conversation(initiator: dict, recipient: dict) -> dict:
        now = datetime.now(timezone.utc)
        doc = {
            "initiator": initiator,
            "recipient": recipient,
            "participant_ids": [initiator["id"], recipient["id"]],
            "unread": {initiator["id"]: 0, recipient["id"]: 0},
            "last_message": None,
            "last_message_at": None,
            "created_at": now,
        }
        result = await mongodb.database[Collections.CONVERSATIONS].insert_one(doc)
        doc["id"] = str(result.inserted_id)
        doc.pop("_id", None)
        return doc

    @staticmethod
    async def get_conversation_for(conversation_id: str, participant_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(conversation_id):
            return None
        doc = await mongodb.database[Collections.CONVERSATIONS].find_one(
            {"_id": ObjectId(conversation_id), "participant_ids": participant_id}
        )
        return MessageRepository._with_id(doc)

    @staticmethod
    async def list_conversations(participant_id: str) -> List[dict]:
        cursor = (
            mongodb.database[Collections.CONVERSATIONS]
            .find({"participant_ids": participant_id})
            .sort([("last_message_at", pymongo.DESCENDING), ("created_at", pymongo.DESCENDING)])
        )
        return [MessageRepository._with_id(doc) async for doc in cursor]

    @staticmethod
    async def count_unread(participant_id: str) -> int:
        pipeline = [
            {"$match": {"participant_ids": participant_id}},
            {"$group": {"_id": None, "total": {"$sum": f"$unread.{participant_id}"}}},
        ]
        result = await mongodb.database[Collections.CONVERSATIONS].aggregate(pipeline).to_list(1)
        return result[0]["total"] if result else 0

    @staticmethod
    async def mark_read(conversation_id: str, participant_id: str):
        await mongodb.database[Collections.CONVERSATIONS].update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {f"unread.{participant_id}": 0}}
        )

    # ---------- Messages ----------

    @staticmethod
    async def add_message(conversation_id: str, sender_id: str, recipient_id: str, content: str) -> dict:
        now = datetime.now(timezone.utc)
        doc = {"conversation_id": conversation_id, "sender_id": sender_id, "content": content, "created_at": now}
        result = await mongodb.database[Collections.MESSAGES].insert_one(doc)
        await mongodb.database[Collections.CONVERSATIONS].update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$set": {"last_message": content, "last_message_at": now},
                "$inc": {f"unread.{recipient_id}": 1},
            }
        )
        doc["id"] = str(result.inserted_id)
        doc.pop("_id", None)
        return doc

    @staticmethod
    async def get_messages(conversation_id: str, limit: int) -> List[dict]:
        cursor = (
            mongodb.database[Collections.MESSAGES]
            .find({"conversation_id": conversation_id})
            .sort("created_at", pymongo.DESCENDING)
            .limit(limit)
        )
        messages = [MessageRepository._with_id(doc) async for doc in cursor]
        return list(reversed(messages))
