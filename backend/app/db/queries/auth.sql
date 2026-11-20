-- backend/app/db/queries/auth.sql
-- Parameterized raw SQL queries for Better Auth workflow

-- name: create_user
INSERT INTO user (id, name, email, email_verified, image, role, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);

-- name: get_user_by_email
SELECT id, name, email, email_verified, image, role, created_at, updated_at
FROM user
WHERE email = ?;

-- name: get_user_by_id
SELECT id, name, email, email_verified, image, role, created_at, updated_at
FROM user
WHERE id = ?;

-- name: create_account
INSERT INTO account (id, user_id, account_id, provider_id, access_token, refresh_token, password, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);

-- name: get_account_by_user_id
SELECT id, user_id, account_id, provider_id, access_token, refresh_token, password, created_at, updated_at
FROM account
WHERE user_id = ? AND provider_id = ?;

-- name: create_session
INSERT INTO session (id, token, user_id, expires_at, ip_address, user_agent, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);

-- name: get_session_by_token
SELECT id, token, user_id, expires_at, ip_address, user_agent, created_at, updated_at
FROM session
WHERE token = ?;

-- name: delete_session_by_token
DELETE FROM session
WHERE token = ?;

-- name: delete_user_sessions
DELETE FROM session
WHERE user_id = ?;
