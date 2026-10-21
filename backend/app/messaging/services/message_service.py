from typing import List
from fastapi import HTTPException, status
from app.core.constants import Messaging, Roles
from app.auth.repository.user_repository import UserRepository
from app.common.identity import get_display_identity
from app.alumni.models.notification import AlumniNotification
from app.alumni.repositories.notification_repository import NotificationRepository
from app.messaging.repositories.message_repository import MessageRepository
from app.messaging.schemas.message_schema import (
    ConversationResponse,
    MessageResponse,
    Participant,
)


class MessageService:

    @staticmethod
    async def _participant_for(entity: dict) -> dict:
        """Display snapshot for a participant."""
        return {"id": entity["id"], "role": entity["role"], **await get_display_identity(entity)}

    @staticmethod
    def _to_response(conversation: dict, viewer_id: str) -> ConversationResponse:
        other = conversation["recipient"] if conversation["initiator"]["id"] == viewer_id else conversation["initiator"]
        return ConversationResponse(
            id=conversation["id"],
            other=Participant(**other),
            last_message=conversation.get("last_message"),
            last_message_at=conversation.get("last_message_at"),
            unread_count=conversation.get("unread", {}).get(viewer_id, 0)
        )

    @staticmethod
    async def start_conversation(entity: dict, recipient_id: str) -> ConversationResponse:
        if entity["role"] not in Messaging.INITIATOR_ROLES:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your role can't start conversations")

        recipient_user = await UserRepository.find_by_id(recipient_id)
        if not recipient_user or recipient_user.role not in Messaging.RECIPIENT_ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You can only message: {', '.join(Messaging.RECIPIENT_ROLES)}"
            )

        conversation = await MessageRepository.find_conversation(entity["id"], recipient_id)
        if not conversation:
            initiator = await MessageService._participant_for(entity)
            recipient = await MessageService._participant_for(
                {"id": recipient_user.id, "name": recipient_user.email, "role": recipient_user.role}
            )
            conversation = await MessageRepository.create_conversation(initiator, recipient)
        return MessageService._to_response(conversation, entity["id"])

    @staticmethod
    async def list_conversations(entity: dict) -> List[ConversationResponse]:
        conversations = await MessageRepository.list_conversations(entity["id"])
        return [MessageService._to_response(c, entity["id"]) for c in conversations]

    @staticmethod
    async def _get_conversation_or_404(conversation_id: str, entity: dict) -> dict:
        conversation = await MessageRepository.get_conversation_for(conversation_id, entity["id"])
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
        return conversation

    @staticmethod
    async def get_messages(conversation_id: str, entity: dict, limit: int) -> List[MessageResponse]:
        await MessageService._get_conversation_or_404(conversation_id, entity)
        messages = await MessageRepository.get_messages(conversation_id, limit)
        await MessageRepository.mark_read(conversation_id, entity["id"])
        return [MessageResponse(**m, is_mine=m["sender_id"] == entity["id"]) for m in messages]

    @staticmethod
    async def send_message(conversation_id: str, entity: dict, content: str) -> MessageResponse:
        conversation = await MessageService._get_conversation_or_404(conversation_id, entity)
        is_initiator = conversation["initiator"]["id"] == entity["id"]
        sender = conversation["initiator"] if is_initiator else conversation["recipient"]
        recipient = conversation["recipient"] if is_initiator else conversation["initiator"]
        was_caught_up = conversation.get("unread", {}).get(recipient["id"], 0) == 0

        message = await MessageRepository.add_message(conversation_id, entity["id"], recipient["id"], content)

        # Ping alumni once per batch of unread messages, not on every message
        if recipient["role"] == Roles.ALUMNI and was_caught_up:
            await NotificationRepository.create_notification(
                AlumniNotification(
                    recipient_id=recipient["id"],
                    title="New message",
                    message=f"{sender['name']}: {content[:120]}",
                    type="message",
                    related_entity_id=conversation_id
                )
            )

        return MessageResponse(**message, is_mine=True)

    @staticmethod
    async def unread_count(entity: dict) -> int:
        return await MessageRepository.count_unread(entity["id"])
