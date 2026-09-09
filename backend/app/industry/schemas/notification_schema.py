from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class NotificationCreate(BaseModel):
    recipient_id: str
    title: str
    message: str
    type: str = "application"
    related_entity_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class NotificationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: str
    recipient_id: str
    title: str
    message: str
    type: str
    related_entity_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    is_read: bool
    created_at: datetime


class UnreadCountResponse(BaseModel):
    unread_count: int
