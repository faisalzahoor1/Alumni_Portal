# app/core/dependencies.py

from fastapi import Header, HTTPException


async def get_token(
    authorization: str = Header(...)
):

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization Header"
        )

    return authorization.split(" ")[1]