from typing import List
from fastapi import APIRouter, Depends, Query
from app.auth.dependensies import require_entity
from app.core.constants import Messaging
from app.messaging.schemas.message_schema import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
    UnreadMessagesResponse,
)
from app.messaging.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["Inbox"])


get_messaging_entity = require_entity(
    Messaging.INITIATOR_ROLES + Messaging.RECIPIENT_ROLES,
    Messaging.REQUIRE_VERIFIED,
    "use the inbox"
)


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(entity: dict = Depends(get_messaging_entity)):
    return await MessageService.list_conversations(entity)


@router.post("/conversations", response_model=ConversationResponse)
async def start_conversation(request: ConversationCreate, entity: dict = Depends(get_messaging_entity)):
    """Open (or reuse) a conversation with a recipient, e.g. a student messaging an alumni."""
    return await MessageService.start_conversation(entity, request.recipient_id)


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: str,
    limit: int = Query(200, ge=1, le=500),
    entity: dict = Depends(get_messaging_entity)
):
    """Latest messages, oldest first. Marks the conversation as read for the viewer."""
    return await MessageService.get_messages(conversation_id, entity, limit)


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(conversation_id: str, request: MessageCreate, entity: dict = Depends(get_messaging_entity)):
    return await MessageService.send_message(conversation_id, entity, request.content)


@router.get("/unread-count", response_model=UnreadMessagesResponse)
async def unread_count(entity: dict = Depends(get_messaging_entity)):
    return UnreadMessagesResponse(unread_count=await MessageService.unread_count(entity))
