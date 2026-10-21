# app/core/config_router.py

from fastapi import APIRouter

from app.core.constants import CV, OTP, Approval, Avatar, Engagement, Feed, Jobs, Messaging, Password, Posts, RegistrationNo, Reports, Roles, University

router = APIRouter(
    prefix="/config",
    tags=["Config"]
)


@router.get("/")
async def get_public_config():
    """
    Public, read-only settings the frontend needs to render forms and validate input.
    """

    return {
        "otp": {
            "length": OTP.LENGTH,
            "expiry_seconds": OTP.EXPIRY_SECONDS,
        },
        "password": {
            "min_length": Password.MIN_LENGTH,
            "max_length": Password.MAX_LENGTH,
        },
        "registration_no": {
            "min_length": RegistrationNo.MIN_LENGTH,
            "max_length": RegistrationNo.MAX_LENGTH,
        },
        "signup_roles": Roles.SIGNUP,
        "feed_author_roles": Roles.FEED_AUTHORS,
        "posts": {
            "title_max_length": Posts.TITLE_MAX_LENGTH,
            "types": Posts.TYPES,
        },
        "jobs": {
            "types": Jobs.TYPES,
            "statuses": Jobs.STATUSES,
            "application_statuses": Jobs.APPLICATION_STATUSES,
        },
        "university": {
            "name": University.NAME,
            "short_name": University.SHORT_NAME,
            "posts_label": University.POSTS_LABEL,
            "author_role": University.AUTHOR_ROLE,
        },
        "approval": {
            "roles": Approval.ROLES,
            "statuses": Approval.STATUSES,
        },
        "reports": {
            "roles": Reports.ROLES,
            "reasons": Reports.REASONS,
            "details_max_length": Reports.DETAILS_MAX_LENGTH,
        },
        "feed": {
            "public": Feed.PUBLIC,
        },
        "engagement": {
            "roles": Engagement.ROLES,
            "require_verified": Engagement.REQUIRE_VERIFIED,
            "reactions": Engagement.REACTIONS,
            "comment_max_length": Engagement.COMMENT_MAX_LENGTH,
        },
        "messaging": {
            "initiator_roles": Messaging.INITIATOR_ROLES,
            "recipient_roles": Messaging.RECIPIENT_ROLES,
            "require_verified": Messaging.REQUIRE_VERIFIED,
            "message_max_length": Messaging.MESSAGE_MAX_LENGTH,
            "poll_interval_seconds": Messaging.POLL_INTERVAL_SECONDS,
        },
        "avatar": {
            "max_size_bytes": Avatar.MAX_SIZE_BYTES,
            "content_types": Avatar.CONTENT_TYPES,
            "extensions": Avatar.EXTENSIONS,
        },
        "cv": {
            "max_size_bytes": CV.MAX_SIZE_BYTES,
            "content_types": CV.CONTENT_TYPES,
            "extensions": CV.EXTENSIONS,
        },
    }
