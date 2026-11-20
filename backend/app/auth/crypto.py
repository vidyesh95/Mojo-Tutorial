# backend/app/auth/crypto.py
import base64
import hashlib
import hmac

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from backend.app.config import settings

# Argon2id password hasher tuned for production security
ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,  # 64 MB
    parallelism=1,
    hash_len=32,
    salt_len=16,
)


def hash_password(password: str) -> str:
    """Hashes a plaintext password using Argon2id."""
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verifies a plaintext password against an Argon2id hash."""
    try:
        return ph.verify(hashed, password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False


def sign_cookie_token(token: str) -> str:
    """
    Signs a session token using HMAC-SHA256 to prevent client-side cookie tampering.
    Returns: <token>.<signature_base64>
    """
    key = settings.BETTER_AUTH_SECRET.encode("utf-8")
    sig = hmac.new(key, token.encode("utf-8"), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode("utf-8").rstrip("=")
    return f"{token}.{sig_b64}"


def unsign_cookie_token(cookie_val: str) -> str | None:
    """
    Validates the HMAC-SHA256 signature on an incoming session cookie.
    Returns the original token if signature matches, or None if tampered.
    """
    if "." not in cookie_val:
        return None
    token, sig_b64 = cookie_val.split(".", 1)

    key = settings.BETTER_AUTH_SECRET.encode("utf-8")
    expected_sig = hmac.new(key, token.encode("utf-8"), hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode("utf-8").rstrip("=")

    if hmac.compare_digest(sig_b64, expected_sig_b64):
        return token
    return None
