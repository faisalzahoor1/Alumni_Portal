from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.auth.services.jwt_service import JWTService
from app.auth.repository.user_repository import UserRepository
from app.auth.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

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
    }

 