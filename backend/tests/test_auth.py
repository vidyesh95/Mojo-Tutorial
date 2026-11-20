# backend/tests/test_auth.py
import asyncio
import pytest
from backend.app.auth.crypto import hash_password, verify_password, sign_cookie_token, unsign_cookie_token
from backend.app.auth.service import sign_up_email, sign_in_email, validate_session, sign_out
from backend.app.db.migrator import run_migrations

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    test_db = str(tmp_path / "auth_test.db")
    monkeypatch.setattr("backend.app.config.settings.DATABASE_PATH", test_db)
    asyncio.run(run_migrations(test_db))

def test_argon2id_hashing():
    password = "SuperSecurePassword123!"
    hashed = hash_password(password)

    # Argon2id hashes start with $argon2id$
    assert hashed.startswith("$argon2id$")
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_hmac_cookie_tampering_protection():
    token = "session_token_xyz_12345"
    signed = sign_cookie_token(token)

    # Valid cookie signature unsigns properly
    unsigned = unsign_cookie_token(signed)
    assert unsigned == token

    # Tampered cookie fails signature check
    tampered = signed[:-4] + "abcd"
    assert unsign_cookie_token(tampered) is None

    # Missing signature separator
    assert unsign_cookie_token("invalid_cookie_without_dot") is None

@pytest.mark.asyncio
async def test_auth_service_lifecycle():
    email = "tester@example.com"
    pwd = "MySecretPassword!2026"
    name = "Alice Tester"

    # 1. Sign up
    user, session, signed_cookie = await sign_up_email(name, email, pwd)
    assert user.email == email
    assert user.name == name
    assert session.user_id == user.id

    # Duplicate sign up should raise ValueError
    with pytest.raises(ValueError):
        await sign_up_email("Duplicate", email, pwd)

    # 2. Validate session
    auth_data = await validate_session(signed_cookie)
    assert auth_data is not None
    valid_user, valid_session = auth_data
    assert valid_user.id == user.id
    assert valid_session.id == session.id

    # 3. Sign in
    signin_user, signin_session, signin_cookie = await sign_in_email(email, pwd)
    assert signin_user.id == user.id
    assert signin_session.token != session.token  # Fresh session token created

    # Invalid password check
    with pytest.raises(ValueError):
        await sign_in_email(email, "WrongPassword!")

    # 4. Sign out
    await sign_out(signin_cookie)
    signed_out_check = await validate_session(signin_cookie)
    assert signed_out_check is None
