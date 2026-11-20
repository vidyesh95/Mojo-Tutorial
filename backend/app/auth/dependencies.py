# backend/app/auth/dependencies.py
from typing import Annotated, Optional
from fastapi import Cookie, Depends, HTTPException, Request, status
from backend.app.auth.schema import Session, User
from backend.app.auth.service import validate_session
from backend.app.config import settings

async def require_session_and_user(
    request: Request,
    session_cookie: Optional[str] = Cookie(default=None, alias=settings.SESSION_COOKIE_NAME)
) -> tuple[User, Session]:
    """Dependency ensuring an authenticated session with an active user."""
    # Also support Authorization: Bearer <signed_token> for testing/mobile
    auth_header = request.headers.get("Authorization")
    token = session_cookie
    if not token and auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]

    auth_data = await validate_session(token)
    if not auth_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid or expired session cookie",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return auth_data

async def require_user(
    auth_data: tuple[User, Session] = Depends(require_session_and_user)
) -> User:
    """Provides the authenticated User instance directly to route handlers."""
    return auth_data[0]

def require_role(allowed_role: str):
    """Guards endpoints ensuring the authenticated user has the required role."""
    async def role_checker(user: User = Depends(require_user)) -> User:
        if user.role != allowed_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: Requires '{allowed_role}' role"
            )
        return user
    return role_checker

CurrentUser = Annotated[User, Depends(require_user)]
