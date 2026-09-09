from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class IndustryNotification(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[str] = None
    recipient_id: str  # industry company user_id
    title: str
    message: str
    type: str = "application"  # "application", "job_status", "system"
    related_entity_id: Optional[str] = None  # e.g., job_id or application_id
    metadata: Optional[Dict[str, Any]] = None
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
