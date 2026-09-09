from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

class Job(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: Optional[str] = None
    company_id: str
    title: str
    description: str
    requirements: List[str] = Field(default_factory=list)
    location: str
    salary_range: Optional[str] = None
    job_type: str  # e.g. Full-time, Part-time, Internship
    status: str = "open"  # open, closed, draft
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
