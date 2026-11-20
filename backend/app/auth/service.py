# backend/app/auth/service.py
import os
import secrets
import uuid
from datetime import UTC, datetime, timedelta

from backend.app.auth.crypto import (
    hash_password,
    sign_cookie_token,
    unsign_cookie_token,
    verify_password,
)
from backend.app.auth.schema import Account, Session, User
from backend.app.config import settings
from backend.app.db.pool import execute, fetch_one
from backend.app.db.verifier import parse_queries

# Load SQL statements from auth.sql
queries_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "queries", "auth.sql")
with open(queries_path, encoding="utf-8") as f:
    AUTH_SQL = parse_queries(f.read())


async def sign_up_email(name: str, email: str, password: str) -> tuple[User, Session, str]:
    """Creates a new User, linked Account with Argon2id hash, and active Session."""
    existing_user = await fetch_one(AUTH_SQL["get_user_by_email"], User, (email,))
    if existing_user:
        raise ValueError("A user with this email address already exists")

    now_iso = datetime.now(UTC).isoformat()
    user_id = str(uuid.uuid4())
    account_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    token = secrets.token_urlsafe(32)

    # 1. Insert User
    await execute(
        AUTH_SQL["create_user"], (user_id, name, email, 0, None, "user", now_iso, now_iso)
    )

    # 2. Insert Account with Argon2id password hash
    hashed_pwd = hash_password(password)
    await execute(
        AUTH_SQL["create_account"],
        (account_id, user_id, email, "credential", None, None, hashed_pwd, now_iso, now_iso),
    )

    # 3. Insert Session
    expires_at = (datetime.now(UTC) + timedelta(days=settings.SESSION_MAX_AGE_DAYS)).isoformat()
    await execute(
        AUTH_SQL["create_session"],
        (session_id, token, user_id, expires_at, None, None, now_iso, now_iso),
    )

    user = await fetch_one(AUTH_SQL["get_user_by_id"], User, (user_id,))
    session = await fetch_one(AUTH_SQL["get_session_by_token"], Session, (token,))
    if not user or not session:
        raise RuntimeError("Failed to create user or session record")
    signed_cookie = sign_cookie_token(token)

    return user, session, signed_cookie


async def sign_in_email(email: str, password: str) -> tuple[User, Session, str]:
    """Validates user credentials via Argon2id and creates a fresh session."""
    user = await fetch_one(AUTH_SQL["get_user_by_email"], User, (email,))
    if not user:
        raise ValueError("Invalid email or password")

    account = await fetch_one(AUTH_SQL["get_account_by_user_id"], Account, (user.id, "credential"))
    if not account or not account.password or not verify_password(password, account.password):
        raise ValueError("Invalid email or password")

    now_iso = datetime.now(UTC).isoformat()
    session_id = str(uuid.uuid4())
    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now(UTC) + timedelta(days=settings.SESSION_MAX_AGE_DAYS)).isoformat()

    await execute(
        AUTH_SQL["create_session"],
        (session_id, token, user.id, expires_at, None, None, now_iso, now_iso),
    )

    session = await fetch_one(AUTH_SQL["get_session_by_token"], Session, (token,))
    if not session:
        raise RuntimeError("Failed to establish session record")
    signed_cookie = sign_cookie_token(token)

    return user, session, signed_cookie


async def validate_session(signed_cookie: str | None) -> tuple[User, Session] | None:
    """Validates an incoming signed session cookie and checks expiration."""
    if not signed_cookie:
        return None

    raw_token = unsign_cookie_token(signed_cookie)
    if not raw_token:
        return None

    session = await fetch_one(AUTH_SQL["get_session_by_token"], Session, (raw_token,))
    if not session:
        return None

    # Check expiration
    expires_dt = datetime.fromisoformat(session.expires_at)
    if datetime.now(UTC) > expires_dt:
        await execute(AUTH_SQL["delete_session_by_token"], (raw_token,))
        return None

    user = await fetch_one(AUTH_SQL["get_user_by_id"], User, (session.user_id,))
    if not user:
        return None

    return user, session


async def sign_out(signed_cookie: str | None):
    """Revokes the current session from the database."""
    if not signed_cookie:
        return
    raw_token = unsign_cookie_token(signed_cookie)
    if raw_token:
        await execute(AUTH_SQL["delete_session_by_token"], (raw_token,))
