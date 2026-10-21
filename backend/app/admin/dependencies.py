from fastapi import Depends, HTTPException, status
from app.auth.dependensies import get_current_user
from app.auth.models.user import User
from app.core.constants import Roles


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != Roles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
