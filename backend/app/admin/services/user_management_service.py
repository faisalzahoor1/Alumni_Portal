import re
from typing import List
from bson import ObjectId
from fastapi import HTTPException, status
from app.database import mongodb
from app.database.collections import Collections
from app.database import redis
from app.core.constants import AdminPortal, Engagement, Roles
from app.admin.schemas.admin_schema import ManagedUser, ManagedUserPage
from app.engagement.repositories.engagement_repository import EngagementRepository

MANAGED_ROLES = [Roles.STUDENT, Roles.ALUMNI, Roles.INDUSTRY]
REACTION_VALUES = [r["value"] for r in Engagement.REACTIONS]


class UserManagementService:

    # ---------- Search ----------

    @staticmethod
    async def search(role: str, search: str | None, page: int) -> ManagedUserPage:
        if role not in MANAGED_ROLES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role must be one of: {', '.join(MANAGED_ROLES)}")
        limit = AdminPortal.USERS_PAGE_SIZE
        skip = (page - 1) * limit
        db = mongodb.database
        pattern = {"$regex": re.escape(search.strip()), "$options": "i"} if search and search.strip() else None

        if role == Roles.STUDENT:
            query = {"$or": [{"name": pattern}, {"email": pattern}, {"registration_no": pattern}]} if pattern else {}
            total = await db[Collections.STUDENTS].count_documents(query)
            cursor = db[Collections.STUDENTS].find(query).sort("name", 1).skip(skip).limit(limit)
            users = [
                ManagedUser(
                    id=str(doc["_id"]), role=role, name=doc.get("name", ""), email=doc.get("email", ""),
                    registration_no=doc.get("registration_no"), avatar_url=doc.get("avatar_url"), created_at=doc.get("created_at")
                )
                async for doc in cursor
            ]
        else:
            profiles = Collections.ALUMNI_PROFILES if role == Roles.ALUMNI else Collections.INDUSTRY_PROFILES
            name_field, avatar_field = ("name", "avatar_url") if role == Roles.ALUMNI else ("company_name", "logo_url")
            query = {"role": role}
            if pattern:
                # Match the login email or the profile's display name
                ids = [ObjectId(p["user_id"]) async for p in db[profiles].find({name_field: pattern}, {"user_id": 1}) if ObjectId.is_valid(p["user_id"])]
                query["$or"] = [{"email": pattern}, {"_id": {"$in": ids}}]
            total = await db[Collections.USERS].count_documents(query)
            docs = [doc async for doc in db[Collections.USERS].find(query).sort("created_at", -1).skip(skip).limit(limit)]
            by_user = {p["user_id"]: p async for p in db[profiles].find({"user_id": {"$in": [str(d["_id"]) for d in docs]}})}
            users = []
            for doc in docs:
                profile = by_user.get(str(doc["_id"]), {})
                users.append(ManagedUser(
                    id=str(doc["_id"]), role=role, name=profile.get(name_field) or doc["email"], email=doc["email"],
                    avatar_url=profile.get(avatar_field), approval_status=doc.get("approval_status"), created_at=doc.get("created_at")
                ))

        return ManagedUserPage(users=users, total=total, page=page, limit=limit, has_more=skip + len(users) < total)

    # ---------- Delete ----------

    @staticmethod
    async def _delete_activity(entity_id: str):
        """Remove everything an account authored or owns, and fix counters on posts it touched."""
        db = mongodb.database
        touched_posts = set()

        # Their posts, with all engagement on them
        own_posts = [str(p["_id"]) async for p in db[Collections.POSTS].find({"author_id": entity_id}, {"_id": 1})]
        if own_posts:
            await db[Collections.COMMENTS].delete_many({"post_id": {"$in": own_posts}})
            await db[Collections.REACTIONS].delete_many({"post_id": {"$in": own_posts}})
            await db[Collections.REPORTS].delete_many({"post_id": {"$in": own_posts}})
            await db[Collections.POSTS].delete_many({"author_id": entity_id})

        # Their comments (and replies to them) on other posts
        comments = [c async for c in db[Collections.COMMENTS].find({"author_id": entity_id}, {"_id": 1, "post_id": 1})]
        if comments:
            comment_ids = [str(c["_id"]) for c in comments]
            touched_posts.update(c["post_id"] for c in comments)
            await db[Collections.COMMENTS].delete_many({"parent_id": {"$in": comment_ids}})
            await db[Collections.COMMENTS].delete_many({"author_id": entity_id})

        # Their reactions and reports
        touched_posts.update([r["post_id"] async for r in db[Collections.REACTIONS].find({"user_id": entity_id}, {"post_id": 1})])
        await db[Collections.REACTIONS].delete_many({"user_id": entity_id})
        await db[Collections.REPORTS].delete_many({"reporter_id": entity_id})

        # Conversations and messages
        conversation_ids = [str(c["_id"]) async for c in db[Collections.CONVERSATIONS].find({"participant_ids": entity_id}, {"_id": 1})]
        if conversation_ids:
            await db[Collections.MESSAGES].delete_many({"conversation_id": {"$in": conversation_ids}})
            await db[Collections.CONVERSATIONS].delete_many({"participant_ids": entity_id})

        await db[Collections.NOTIFICATIONS].delete_many({"recipient_id": entity_id})

        for post_id in touched_posts - set(own_posts):
            if ObjectId.is_valid(post_id):
                await EngagementRepository.refresh_counts(post_id, REACTION_VALUES)

    @staticmethod
    async def delete(role: str, user_id: str) -> dict:
        if role not in MANAGED_ROLES or not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db = mongodb.database

        if role == Roles.STUDENT:
            student = await db[Collections.STUDENTS].find_one({"_id": ObjectId(user_id)})
            if not student:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            await UserManagementService._delete_activity(user_id)
            await db[Collections.STUDENTS].delete_one({"_id": student["_id"]})
            await redis.redis_client.delete(f"refresh:{student['registration_no']}")
            return {"message": f"Deleted student {student.get('name') or student['registration_no']}"}

        user = await db[Collections.USERS].find_one({"_id": ObjectId(user_id), "role": role})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await UserManagementService._delete_activity(user_id)
        if role == Roles.ALUMNI:
            await db[Collections.ALUMNI_PROFILES].delete_many({"user_id": user_id})
        else:
            job_ids = [str(j["_id"]) async for j in db[Collections.JOBS].find({"company_id": user_id}, {"_id": 1})]
            await db[Collections.APPLICATIONS].delete_many({"job_id": {"$in": job_ids}})
            await db[Collections.JOBS].delete_many({"company_id": user_id})
            await db[Collections.INDUSTRY_PROFILES].delete_many({"user_id": user_id})
        await db[Collections.APPLICATIONS].delete_many({"applicant_user_id": user_id})
        await db[Collections.USERS].delete_one({"_id": user["_id"]})
        await redis.redis_client.delete(f"refresh:{user_id}")
        return {"message": f"Deleted {role} account {user['email']}"}
