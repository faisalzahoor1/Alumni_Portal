from app.industry.repositories.application_repository import ApplicationRepository
from app.industry.models.application import Application
from app.industry.schemas.application_schema import ApplicationCreate, ApplicationUpdate
from app.industry.services.job_service import JobService
from fastapi import HTTPException
from typing import List

class ApplicationService:
    
    @staticmethod
    async def create_application(applicant_id: str, data: ApplicationCreate) -> Application:
        # Verify job exists and is open
        job = await JobService.get_job(data.job_id)
        if job.status != "open":
            raise HTTPException(status_code=400, detail="Job is not open for applications")
            
        new_app = Application(applicant_user_id=applicant_id, **data.model_dump())
        saved_app = await ApplicationRepository.create_application(new_app)

        # Trigger notification to the employer company
        try:
            from app.industry.services.notification_service import NotificationService
            from app.industry.schemas.notification_schema import NotificationCreate
            await NotificationService.create_notification(
                NotificationCreate(
                    recipient_id=job.company_id,
                    title="New Job Application",
                    message=f"A new application has been submitted for '{job.title}'.",
                    type="application",
                    related_entity_id=saved_app.id,
                    metadata={"job_id": job.id, "job_title": job.title}
                )
            )
        except Exception:
            pass

        return saved_app

    @staticmethod
    async def get_applications_for_job(company_id: str, job_id: str) -> List[Application]:
        job = await JobService.get_job(job_id)
        if job.company_id != company_id:
            raise HTTPException(status_code=403, detail="Not authorized to view these applications")
            
        return await ApplicationRepository.get_all_by_job(job_id)
        
    @staticmethod
    async def update_application_status(company_id: str, app_id: str, data: ApplicationUpdate) -> Application:
        app = await ApplicationRepository.get_by_id(app_id)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")
            
        # Verify company owns the job
        job = await JobService.get_job(app.job_id)
        if job.company_id != company_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this application")
            
        return await ApplicationRepository.update_status(app_id, data.status)
