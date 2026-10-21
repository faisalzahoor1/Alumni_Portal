from pydantic import BaseModel


class VerifyEmailResponse(BaseModel):
    """
    Email verified. Roles that need admin approval get a message and no tokens;
    everyone else is signed in straight away.
    """

    message: str

    approval_status: str | None = None

    access_token: str | None = None

    refresh_token: str | None = None

    token_type: str = "bearer"

    role: str | None = None
