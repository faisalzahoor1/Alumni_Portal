import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from app.database import cloudinary_config


class MediaService:

    @staticmethod
    async def upload_image(file: UploadFile, folder: str = "alumni_portal/posts") -> str:
        if file.content_type and not (
            file.content_type.startswith("image/") or
            file.content_type in ["application/pdf", "image/jpeg", "image/png", "image/webp", "image/gif"]
        ):
            raise HTTPException(status_code=400, detail="Only image and document files are supported")

        try:
            result = cloudinary.uploader.upload(
                file.file,
                resource_type="auto",
                folder=folder
            )
            return result.get("secure_url") or result.get("url")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload media: {str(e)}"
            )
