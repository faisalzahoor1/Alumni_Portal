from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class IndustryProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None
    employee_count: Optional[str] = None
    industry_type: Optional[str] = None

class IndustryProfileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: str
    user_id: str
    company_name: str
    description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None
    employee_count: Optional[str] = None
    industry_type: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
