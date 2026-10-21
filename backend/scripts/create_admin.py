"""
Create (or reset the password of) an admin account for the admin portal.

Usage, from the backend folder:
    .venv/bin/python -m scripts.create_admin --email admin@example.com --name "Portal Admin"
The password is prompted for, or pass --password.
"""

import argparse
import asyncio
import getpass
from datetime import datetime, timezone

from app.core.constants import Password, Roles
from app.core.security import hash_password
from app.database import mongodb
from app.database.collections import Collections
from app.database.mongodb import connect_to_mongodb


async def main(email: str, password: str, name: str | None):
    await connect_to_mongodb()
    users = mongodb.database[Collections.USERS]
    now = datetime.now(timezone.utc)

    existing = await users.find_one({"email": email})
    if existing and existing["role"] != Roles.ADMIN:
        raise SystemExit(f"{email} already belongs to a {existing['role']} account; use another email.")

    if existing:
        await users.update_one({"_id": existing["_id"]}, {"$set": {"hashed_password": hash_password(password), "updated_at": now}})
        user_id = str(existing["_id"])
        print(f"Password reset for admin {email}")
    else:
        result = await users.insert_one({
            "email": email,
            "hashed_password": hash_password(password),
            "role": Roles.ADMIN,
            "is_verified": True,
            "created_at": now,
            "updated_at": now,
        })
        user_id = str(result.inserted_id)
        print(f"Created admin {email}")

    if name:
        await mongodb.database[Collections.ADMIN_PROFILES].update_one(
            {"user_id": user_id},
            {"$set": {"name": name, "updated_at": now}, "$setOnInsert": {"user_id": user_id, "avatar_url": None, "created_at": now}},
            upsert=True
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an admin account")
    parser.add_argument("--email", required=True)
    parser.add_argument("--name")
    parser.add_argument("--password")
    args = parser.parse_args()

    password = args.password or getpass.getpass("Password: ")
    if not Password.MIN_LENGTH <= len(password) <= Password.MAX_LENGTH:
        raise SystemExit(f"Password must be {Password.MIN_LENGTH}-{Password.MAX_LENGTH} characters")

    asyncio.run(main(args.email.strip().lower(), password, args.name))
