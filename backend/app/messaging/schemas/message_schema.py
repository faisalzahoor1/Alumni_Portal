from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from app.core.constants import Messaging


class Participant(BaseModel):
    id: str
    name: str
    role: str
    avatar_url: Optional[str] = None


class ConversationCreate(BaseModel):
    recipient_id: str


class ConversationResponse(BaseModel):
    id: str
    other: Participant
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    unread_count: int = 0


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=Messaging.MESSAGE_MAX_LENGTH)

    @field_validator("content")
    @classmethod
    def strip_content(cls, content: str):
        content = content.strip()
        if not content:
            raise ValueError("Message cannot be empty")
        return content


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_id: str
    content: str
    created_at: datetime
    is_mine: bool = False


class UnreadMessagesResponse(BaseModel):
    unread_count: int
