from app.database import mongodb
from bson import ObjectId
from app.auth.models.user import User
from app.database.collections import Collections
from datetime import datetime

class UserRepository:

    @staticmethod
    async def create_user(user: User) -> str:

        user_dict = user.model_dump()

        result = await mongodb.database[Collections.USERS].insert_one(user_dict)

        return str(result.inserted_id)

    @staticmethod
    async def find_by_email(email: str) -> User | None:

        document = await mongodb.database[
            Collections.USERS
        ].find_one(
            {
                "email": email
            }
        )

        if not document:
            return None

        document["id"] = str(document.pop("_id"))

        return User(**document)
    @staticmethod
    async def find_by_id(user_id: str) -> User | None:

        document = await mongodb.database[
            Collections.USERS
        ].find_one(
            {
                "_id": ObjectId(user_id)
            }
        )

        if not document:
            return None

        document["id"] = str(document.pop("_id"))

        return User(**document)
    @staticmethod
    async def verify_user(email: str):

        await mongodb.database[
            Collections.USERS
        ].update_one(
            {
                "email": email
            },
            {
                "$set": {
                    "is_verified": True
                }
            }
        )

    @staticmethod
    async def update_password(
        email: str,
        hashed_password: str
    ):

        await mongodb.database[
            Collections.USERS
        ].update_one(
            {
                "email": email
            },
            {
                "$set": {
                    "hashed_password": hashed_password
                }
            }
        )
    @staticmethod
    async def delete_user(email: str):

        await mongodb.database[
            Collections.USERS
        ].delete_one(
            {
                "email": email
            }
        )
    # @staticmethod
    # async def update_unverified_user(email: str,hashed_password: str,role: str):
    #     await mongodb.database[Collections.USERS].update_one(
    #         {"email": email},
    #         {
    #             "$set": {
    #                 "is_verified": True,
    #                 "updated_at": datetime.utcnow()
    #             }
    #         }
    #     )