from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AdminNotification(BaseModel):
    """Shared by all admins: registration requests, post reports."""

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[str] = None
    title: str
    message: str
    type: str  # "registration" | "report"
    related_entity_id: Optional[str] = None  # user id or post id
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
