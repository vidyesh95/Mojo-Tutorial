# backend/app/auth/router.py
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from backend.app.auth.dependencies import require_session_and_user
from backend.app.auth.schema import Session, SessionResponse, SignInRequest, SignUpRequest, User
from backend.app.auth.service import sign_in_email, sign_out, sign_up_email
from backend.app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Better Auth"])

def set_session_cookie(response: Response, signed_token: str):
    """Sets an HMAC-signed HttpOnly, SameSite=Lax cookie matching Better Auth specs."""
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=signed_token,
        max_age=settings.SESSION_MAX_AGE_DAYS * 24 * 60 * 60,
        httponly=True,
        samesite="lax",
        secure=settings.ENVIRONMENT != "development"
    )

@router.post("/sign-up/email", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def handle_sign_up(payload: SignUpRequest, response: Response):
    """Registers a new user account with Argon2id password hashing."""
    try:
        user, session, signed_token = await sign_up_email(payload.name, str(payload.email), payload.password)
        set_session_cookie(response, signed_token)
        return SessionResponse(user=user, session=session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/sign-in/email", response_model=SessionResponse)
async def handle_sign_in(payload: SignInRequest, response: Response):
    """Authenticates credentials against Argon2id hash and establishes a new session."""
    try:
        user, session, signed_token = await sign_in_email(str(payload.email), payload.password)
        set_session_cookie(response, signed_token)
        return SessionResponse(user=user, session=session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/sign-out")
async def handle_sign_out(
    response: Response,
    session_cookie: str = Cookie(default=None, alias=settings.SESSION_COOKIE_NAME)
):
    """Revokes the current session and clears the session cookie."""
    await sign_out(session_cookie)
    response.delete_cookie(key=settings.SESSION_COOKIE_NAME)
    return {"success": True, "message": "Successfully signed out"}

@router.get("/get-session", response_model=SessionResponse)
async def handle_get_session(
    auth_data: tuple[User, Session] = Depends(require_session_and_user)
):
    """Returns the currently active user and session."""
    user, session = auth_data
    return SessionResponse(user=user, session=session)
