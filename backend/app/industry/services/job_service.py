from app.industry.repositories.job_repository import JobRepository
from app.industry.models.job import Job
from app.industry.schemas.job_schema import JobCreate, JobUpdate
from fastapi import HTTPException
from typing import List

class JobService:
    
    @staticmethod
    async def create_job(company_id: str, data: JobCreate) -> Job:
        new_job = Job(company_id=company_id, **data.model_dump())
        return await JobRepository.create_job(new_job)

    @staticmethod
    async def get_job(job_id: str) -> Job:
        job = await JobRepository.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
        
    @staticmethod
    async def get_jobs_by_company(company_id: str) -> List[Job]:
        return await JobRepository.get_all_by_company(company_id)

    @staticmethod
    async def update_job(job_id: str, company_id: str, data: JobUpdate) -> Job:
        job = await JobService.get_job(job_id)
        if job.company_id != company_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this job")
            
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided to update")
            
        return await JobRepository.update_job(job_id, update_data)
        
    @staticmethod
    async def delete_job(job_id: str, company_id: str):
        job = await JobService.get_job(job_id)
        if job.company_id != company_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this job")
        await JobRepository.delete_job(job_id)
