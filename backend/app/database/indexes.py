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