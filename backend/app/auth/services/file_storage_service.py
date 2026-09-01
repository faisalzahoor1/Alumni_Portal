import cloudinary.uploader

from fastapi import UploadFile
from app.database import cloudinary_config

class FileStorageService:

    @staticmethod
    async def upload_cv(file: UploadFile):

        result = cloudinary.uploader.upload(
            file.file,
            resource_type="raw",
            folder="alumni_portal"
        )

        return {
            "file_url": result["secure_url"]
        }