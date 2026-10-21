from typing import List
from bson import ObjectId
from fastapi import HTTPException, status
from loguru import logger
from app.database import mongodb
from app.database.collections import Collections
from app.core.config import settings
from app.core.constants import Approval, Roles, University
from app.auth.services.email_service import EmailService
from app.admin.schemas.admin_schema import RegistrationDecisionResponse, RegistrationResponse
from app.alumni.models.notification import AlumniNotification
from app.industry.models.notification import IndustryNotification
from app.alumni.repositories.notification_repository import NotificationRepository as AlumniNotificationRepository
from app.industry.repositories.notification_repository import NotificationRepository as IndustryNotificationRepository


class RegistrationService:

    @staticmethod
    async def _display_name(user: dict) -> str | None:
        user_id = str(user["_id"])
        if user["role"] == Roles.ALUMNI:
            profile = await mongodb.database[Collections.ALUMNI_PROFILES].find_one({"user_id": user_id})
            return profile.get("name") if profile else None
        if user["role"] == Roles.INDUSTRY:
            profile = await mongodb.database[Collections.INDUSTRY_PROFILES].find_one({"user_id": user_id})
            return profile.get("company_name") if profile else None
        return None

    @staticmethod
    async def _to_response(user: dict) -> RegistrationResponse:
        return RegistrationResponse(
            id=str(user["_id"]),
            email=user["email"],
            role=user["role"],
            name=await RegistrationService._display_name(user),
            approval_status=user.get("approval_status") or Approval.APPROVED,
            created_at=user.get("created_at")
        )

    @staticmethod
    async def list(approval_status: str) -> List[RegistrationResponse]:
        if approval_status not in Approval.STATUSES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Status must be one of: {', '.join(Approval.STATUSES)}")
        # Accounts created before approvals existed have no status and count as approved
        status_query = {"$in": [Approval.APPROVED, None]} if approval_status == Approval.APPROVED else approval_status
        cursor = mongodb.database[Collections.USERS].find(
            {"role": {"$in": Approval.ROLES}, "is_verified": True, "approval_status": status_query}
        ).sort("created_at", -1)
        return [await RegistrationService._to_response(user) async for user in cursor]

    @staticmethod
    async def count_pending() -> int:
        return await mongodb.database[Collections.USERS].count_documents(
            {"role": {"$in": Approval.ROLES}, "is_verified": True, "approval_status": Approval.PENDING}
        )

    @staticmethod
    async def decide(user_id: str, approve: bool) -> RegistrationDecisionResponse:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
        users = mongodb.database[Collections.USERS]
        user = await users.find_one({"_id": ObjectId(user_id), "role": {"$in": Approval.ROLES}, "is_verified": True})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")

        new_status = Approval.APPROVED if approve else Approval.REJECTED
        await users.update_one({"_id": user["_id"]}, {"$set": {"approval_status": new_status}})
        user["approval_status"] = new_status

        if approve:
            subject = f"{University.SHORT_NAME} Alumni Portal - Your account is approved"
            body = (
                f"Hello,\n\nGood news! An admin has approved your {user['role']} account.\n\n"
                f"You can now sign in with your email and password:\n{settings.FRONTEND_URL}/auth/login\n\n"
                f"Regards,\n{University.NAME} Alumni Portal"
            )
            welcome = {
                "recipient_id": user_id,
                "title": "Welcome aboard!",
                "message": "An admin approved your account. Complete your profile so others can find you.",
                "type": "system",
            }
            if user["role"] == Roles.ALUMNI:
                await AlumniNotificationRepository.create_notification(AlumniNotification(**welcome))
            else:
                await IndustryNotificationRepository.create_notification(IndustryNotification(**welcome))
        else:
            subject = f"{University.SHORT_NAME} Alumni Portal - Registration update"
            body = (
                f"Hello,\n\nAfter review, your {user['role']} registration was not approved.\n"
                f"If you think this is a mistake, please contact the university.\n\n"
                f"Regards,\n{University.NAME} Alumni Portal"
            )

        # The decision stands even if the email can't be delivered; the admin is told either way
        email_sent = True
        try:
            await EmailService.send_email(user["email"], subject, body)
        except Exception as e:
            email_sent = False
            logger.warning(f"Could not email registration decision to {user['email']}: {e}")

        return RegistrationDecisionResponse(
            registration=await RegistrationService._to_response(user),
            email_sent=email_sent
        )
