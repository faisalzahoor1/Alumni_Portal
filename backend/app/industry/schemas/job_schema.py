from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class JobCreate(BaseModel):
    title: str
    description: str
    requirements: List[str] = []
    location: str
    salary_range: Optional[str] = None
    job_type: str

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = None
    status: Optional[str] = None

class JobResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: str
    company_id: str
    title: str
    description: str
    requirements: List[str]
    location: str
    salary_range: Optional[str] = None
    job_type: str
    status: str
    
    created_at: datetime
    updated_at: datetime
