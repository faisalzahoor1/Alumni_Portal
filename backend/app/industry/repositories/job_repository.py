from app.database import mongodb
from bson import ObjectId
from app.industry.models.job import Job
from app.database.collections import Collections
from datetime import datetime
from typing import List

class JobRepository:
    
    @staticmethod
    async def create_job(job: Job) -> Job:
        job_dict = job.model_dump()
        result = await mongodb.database[Collections.JOBS].insert_one(job_dict)
        job.id = str(result.inserted_id)
        return job
        
    @staticmethod
    async def get_by_id(job_id: str) -> Job | None:
        if not ObjectId.is_valid(job_id):
            return None
        document = await mongodb.database[Collections.JOBS].find_one({"_id": ObjectId(job_id)})
        if not document:
            return None
        document["id"] = str(document.pop("_id"))
        return Job(**document)

    @staticmethod
    async def get_all_by_company(company_id: str) -> List[Job]:
        cursor = mongodb.database[Collections.JOBS].find({"company_id": company_id})
        jobs = []
        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            jobs.append(Job(**document))
        return jobs

    @staticmethod
    async def update_job(job_id: str, update_data: dict) -> Job | None:
        if not ObjectId.is_valid(job_id):
            return None
        update_data["updated_at"] = datetime.utcnow()
        await mongodb.database[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {"$set": update_data}
        )
        return await JobRepository.get_by_id(job_id)
        
    @staticmethod
    async def delete_job(job_id: str):
        if not ObjectId.is_valid(job_id):
            return
        await mongodb.database[Collections.JOBS].delete_one({"_id": ObjectId(job_id)})
