from app.database import mongodb
from bson import ObjectId
from app.industry.models.application import Application
from app.database.collections import Collections
from datetime import datetime
from typing import List

class ApplicationRepository:
    
    @staticmethod
    async def create_application(application: Application) -> Application:
        app_dict = application.model_dump()
        result = await mongodb.database[Collections.APPLICATIONS].insert_one(app_dict)
        application.id = str(result.inserted_id)
        return application
        
    @staticmethod
    async def get_by_id(app_id: str) -> Application | None:
        if not ObjectId.is_valid(app_id):
            return None
        document = await mongodb.database[Collections.APPLICATIONS].find_one({"_id": ObjectId(app_id)})
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        return Application(**document)

    @staticmethod
    async def get_all_by_job(job_id: str) -> List[Application]:
        cursor = mongodb.database[Collections.APPLICATIONS].find({"job_id": job_id})
        apps = []
        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            apps.append(Application(**document))
        return apps
        
    @staticmethod
    async def get_all_by_applicant(applicant_user_id: str) -> List[Application]:
        cursor = mongodb.database[Collections.APPLICATIONS].find({"applicant_user_id": applicant_user_id})
        apps = []
        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            apps.append(Application(**document))
        return apps

    @staticmethod
    async def update_status(app_id: str, status: str) -> Application | None:
        await mongodb.database[Collections.APPLICATIONS].update_one(
            {"_id": ObjectId(app_id)},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        return await ApplicationRepository.get_by_id(app_id)
