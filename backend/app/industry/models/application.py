from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class Application(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: Optional[str] = None
    job_id: str
    applicant_user_id: str
    resume_link: Optional[str] = None
    cover_letter: Optional[str] = None
    status: str = "pending"  # pending, reviewed, accepted, rejected
    
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
