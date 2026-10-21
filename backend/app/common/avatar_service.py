# app/common/avatar_service.py

import cloudinary.uploader
from fastapi import HTTPException, UploadFile, status

from app.core.constants import Avatar
from app.database import cloudinary_config  # noqa: F401  (configures cloudinary)
from app.database import mongodb
from app.database.collections import Collections


class AvatarService:

    @staticmethod
    async def upload(file: UploadFile, folder: str) -> str:
        """Validate an image against the Avatar rules and upload it as a square crop."""
        if file.content_type not in Avatar.CONTENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Profile pictures must be one of: {', '.join(Avatar.EXTENSIONS)}"
            )

        contents = await file.read()
        if len(contents) > Avatar.MAX_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Profile picture must not exceed {Avatar.MAX_SIZE_BYTES // (1024 * 1024)} MB"
            )

        try:
            result = cloudinary.uploader.upload(
                contents,
                resource_type="image",
                folder=folder,
                transformation=[{
                    "width": Avatar.SIZE_PX,
                    "height": Avatar.SIZE_PX,
                    "crop": "fill",
                    "gravity": "face",
                }]
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to upload profile picture: {e}"
            )
        return result.get("secure_url") or result.get("url")

    @staticmethod
    async def propagate(entity_id: str, avatar_url: str):
        """Posts, comments and conversations keep a copy of the author's picture; refresh it everywhere."""
        db = mongodb.database
        await db[Collections.POSTS].update_many({"author_id": entity_id}, {"$set": {"author_avatar": avatar_url}})
        await db[Collections.COMMENTS].update_many({"author_id": entity_id}, {"$set": {"author_avatar": avatar_url}})
        await db[Collections.CONVERSATIONS].update_many({"initiator.id": entity_id}, {"$set": {"initiator.avatar_url": avatar_url}})
        await db[Collections.CONVERSATIONS].update_many({"recipient.id": entity_id}, {"$set": {"recipient.avatar_url": avatar_url}})
