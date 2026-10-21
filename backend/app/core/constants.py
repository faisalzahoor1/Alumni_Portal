# app/core/constants.py
#
# Single source of truth for roles, option lists and validation rules.
# The frontend reads these through GET /api/v1/config/, so change them here only.

class Roles:
    STUDENT = "student"
    ALUMNI = "alumni"
    INDUSTRY = "industry"
    ADMIN = "admin"

    # Roles that can self-register with email + OTP (students use university SSO)
    SIGNUP = [
        {"value": ALUMNI, "label": "Alumni", "description": "Graduate of the university"},
        {"value": INDUSTRY, "label": "Industry", "description": "Company or recruiter"},
    ]

    # Roles whose posts appear in the community feed
    FEED_AUTHORS = [
        {"value": ALUMNI, "label": "Alumni"},
        {"value": INDUSTRY, "label": "Industry"},
    ]


class TokenType:
    ACCESS = "access"
    REFRESH = "refresh"

class OTP:
    LENGTH = 6                 # OTP will have 6 digits
    EXPIRY_SECONDS = 300      # Expires after 5 minutes


class RedisKeys:
    OTP = "otp"


class Password:
    MIN_LENGTH = 8
    MAX_LENGTH = 64


class RegistrationNo:
    MIN_LENGTH = 5
    MAX_LENGTH = 20


class Posts:
    TITLE_MAX_LENGTH = 250

    # job_fields: the post form shows job title / company / apply URL for this type
    TYPES = [
        {"value": "general", "label": "General"},
        {"value": "achievement", "label": "Achievement"},
        {"value": "job_opportunity", "label": "Job opportunity", "job_fields": True},
        {"value": "announcement", "label": "Announcement"},
    ]


class Jobs:
    TYPES = ["Full-time", "Part-time", "Internship", "Contract", "Remote"]
    STATUSES = ["open", "closed", "draft"]
    APPLICATION_STATUSES = ["pending", "reviewed", "accepted", "rejected"]


class CV:
    MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
    CONTENT_TYPES = ["application/pdf"]
    EXTENSIONS = [".pdf"]


class Feed:
    # Logged-out visitors can read the community feed and its comments
    PUBLIC = True


class Engagement:
    # Roles that can react, comment and reply on community feed posts
    ROLES = [Roles.STUDENT, Roles.ALUMNI, Roles.INDUSTRY, Roles.ADMIN]
    # Only verified accounts (SSO students, email-verified alumni/industry) may engage
    REQUIRE_VERIFIED = True
    REACTIONS = [
        {"value": "like", "label": "Like"},
        {"value": "dislike", "label": "Dislike"},
    ]
    COMMENT_MAX_LENGTH = 1000


class Messaging:
    # Initiators can start a conversation with recipients; both sides can reply
    INITIATOR_ROLES = [Roles.STUDENT]
    RECIPIENT_ROLES = [Roles.ALUMNI]
    REQUIRE_VERIFIED = True
    MESSAGE_MAX_LENGTH = 2000
    POLL_INTERVAL_SECONDS = 5


class Avatar:
    # Profile pictures for every role (alumni photo, industry logo, student photo)
    MAX_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB
    CONTENT_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".gif"]
    SIZE_PX = 400  # stored as a square crop, centred on the face when one is found


class Approval:
    # Self-registered roles that need an admin's approval after verifying their email
    ROLES = [Roles.ALUMNI, Roles.INDUSTRY]
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUSES = [PENDING, APPROVED, REJECTED]


class University:
    NAME = "COMSATS University Islamabad"
    SHORT_NAME = "COMSATS"
    POSTS_LABEL = "COMSATS Posts"
    # Posts written by this role are official university posts, shown on their own page
    AUTHOR_ROLE = Roles.ADMIN


class Reports:
    # Roles that can report posts to the admins
    ROLES = [Roles.STUDENT, Roles.ALUMNI, Roles.INDUSTRY]
    REASONS = [
        {"value": "spam", "label": "Spam or scam"},
        {"value": "harassment", "label": "Harassment or hate speech"},
        {"value": "inappropriate", "label": "Inappropriate content"},
        {"value": "misinformation", "label": "False information"},
        {"value": "other", "label": "Something else"},
    ]
    DETAILS_MAX_LENGTH = 500
    PENDING = "pending"
    DISMISSED = "dismissed"
    ACTIONED = "actioned"


class AdminPortal:
    USERS_PAGE_SIZE = 20
