# app/database/indexes.py

# from app.database.mongodb import database
from app.database import mongodb

from app.database.collections import Collections


async def create_indexes():

    await mongodb.database[Collections.USERS].create_index(
        "email",
        unique=True
    )
        
    await mongodb.database[Collections.STUDENTS].create_index(
        "registration_no",
        unique=True
    )

    await mongodb.database[Collections.STUDENTS].create_index(
            "email",
            unique=True
    )

    await mongodb.database[Collections.POSTS].create_index(
        "created_at"
    )

    await mongodb.database[Collections.NOTIFICATIONS].create_index(
        "student_id"
    )

    # Industry Module Indexes
    await mongodb.database[Collections.INDUSTRY_PROFILES].create_index(
        "user_id",
        unique=True
    )

    await mongodb.database[Collections.JOBS].create_index(
        "company_id"
    )

    await mongodb.database[Collections.JOBS].create_index(
        "created_at"
    )

    await mongodb.database[Collections.APPLICATIONS].create_index(
        "job_id"
    )

    await mongodb.database[Collections.APPLICATIONS].create_index(
        "applicant_user_id"
    )

    # Alumni Module Indexes
    await mongodb.database[Collections.ALUMNI_PROFILES].create_index(
        "user_id",
        unique=True
    )

    # Posts Indexes
    await mongodb.database[Collections.POSTS].create_index(
        "author_id"
    )

    await mongodb.database[Collections.POSTS].create_index(
        "author_role"
    )

    await mongodb.database[Collections.NOTIFICATIONS].create_index(
        "recipient_id"
    )

    # Engagement Indexes
    await mongodb.database[Collections.REACTIONS].create_index(
        [("post_id", 1), ("user_id", 1)],
        unique=True
    )

    await mongodb.database[Collections.COMMENTS].create_index(
        [("post_id", 1), ("created_at", 1)]
    )

    # Admin Indexes
    await mongodb.database[Collections.REPORTS].create_index(
        [("post_id", 1), ("status", 1)]
    )

    await mongodb.database[Collections.REPORTS].create_index(
        [("post_id", 1), ("reporter_id", 1), ("status", 1)]
    )

    await mongodb.database[Collections.ADMIN_NOTIFICATIONS].create_index(
        "created_at"
    )

    await mongodb.database[Collections.ADMIN_PROFILES].create_index(
        "user_id",
        unique=True
    )

    await mongodb.database[Collections.USERS].create_index(
        "approval_status"
    )

    # Messaging Indexes
    await mongodb.database[Collections.CONVERSATIONS].create_index(
        [("initiator.id", 1), ("recipient.id", 1)],
        unique=True
    )

    await mongodb.database[Collections.CONVERSATIONS].create_index(
        [("participant_ids", 1), ("last_message_at", -1)]
    )

    await mongodb.database[Collections.MESSAGES].create_index(
        [("conversation_id", 1), ("created_at", 1)]
    )
