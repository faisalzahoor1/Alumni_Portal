from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import Reports


class PostReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[str] = None
    post_id: str
    reporter_id: str
    reporter_role: str
    reporter_name: str
    reason: str
    details: Optional[str] = None
    status: str = Reports.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
