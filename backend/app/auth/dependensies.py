from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.auth.services.jwt_service import JWTService
from app.auth.repository.user_repository import UserRepository
from app.auth.models.user import User
from app.core.constants import Feed

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
# Same scheme, but a missing token yields None instead of a 401 (public endpoints)
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = JWTService.verify(token)
        user_id: str = payload.get("sub") or payload.get("id")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await UserRepository.find_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_industry_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "industry":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Requires industry role."
        )
    return current_user

async def get_current_alumni_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "alumni":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Requires alumni role."
        )
    return current_user

async def get_current_authenticated_entity(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = JWTService.verify(token)
        sub: str = payload.get("sub") or payload.get("id")
        role: str = payload.get("role")
        if not sub:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if role == "student":
        from app.student.repository.student_repository import StudentRepository
        student = await StudentRepository.find_by_registration_no(sub)
        if not student:
            # Fallback check by id
            student = await StudentRepository.find_by_id(sub)
        if not student:
            raise credentials_exception
        return {
            "id": student.id or student.registration_no,
            "sub": student.registration_no,
            "role": "student",
            "name": student.name,
            "email": student.email,
            "avatar_url": student.avatar_url,
            # Students authenticate through university SSO, which verifies them
            "is_verified": True,
        }

    user = await UserRepository.find_by_id(sub)
    if not user:
        raise credentials_exception
    return {
        "id": user.id,
        "sub": user.id,
        "role": user.role,
        "email": user.email,
        "name": user.email,
        "is_verified": user.is_verified,
    }


async def get_optional_authenticated_entity(token: Optional[str] = Depends(optional_oauth2_scheme)) -> Optional[dict]:
    """The signed-in entity, or None for anonymous visitors and invalid/expired tokens."""
    if not token:
        return None
    try:
        return await get_current_authenticated_entity(token)
    except HTTPException:
        return None


async def get_feed_viewer(entity: Optional[dict] = Depends(get_optional_authenticated_entity)) -> Optional[dict]:
    """Feed access: anonymous visitors are allowed only while the feed is public."""
    if entity is None and not Feed.PUBLIC:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sign in to view the community feed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return entity


def require_entity(roles: list, require_verified: bool, action: str):
    """Dependency factory: the signed-in entity must have one of `roles` (and be verified if required)."""
    async def dependency(entity: dict = Depends(get_current_authenticated_entity)) -> dict:
        if entity["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Your account type can't {action}"
            )
        if require_verified and not entity.get("is_verified"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Only verified accounts can {action}"
            )
        return entity
    return dependency

 