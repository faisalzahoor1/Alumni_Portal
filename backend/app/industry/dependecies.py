from fastapi import Depends, HTTPException, status
from app.auth.models.user import User
from app.auth.dependensies import get_current_user


async def get_current_industry_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "industry":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Requires industry role."
        )
    return current_user
