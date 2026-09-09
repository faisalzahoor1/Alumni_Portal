from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    job_id: str
    resume_link: Optional[str] = None
    cover_letter: Optional[str] = None

class ApplicationUpdate(BaseModel):
    status: str

class ApplicationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: str
    job_id: str
    applicant_user_id: str
    resume_link: Optional[str] = None
    cover_letter: Optional[str] = None
    status: str
    
    applied_at: datetime
    updated_at: datetime
