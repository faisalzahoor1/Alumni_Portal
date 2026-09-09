from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class IndustryProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: Optional[str] = None
    user_id: str
    company_name: str
    description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None
    employee_count: Optional[str] = None
    industry_type: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
