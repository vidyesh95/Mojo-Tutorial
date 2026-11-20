-- backend/app/db/queries/items.sql
-- Parameterized raw SQL queries for Application Domain Items & Scoring

-- name: create_item
INSERT INTO items (id, owner_id, title, payload_score, created_at)
VALUES (?, ?, ?, ?, ?);

-- name: get_item_by_id
SELECT id, owner_id, title, payload_score, created_at
FROM items
WHERE id = ?;

-- name: list_user_items
SELECT id, owner_id, title, payload_score, created_at
FROM items
WHERE owner_id = ?
ORDER BY created_at DESC;

-- name: update_item_score
UPDATE items
SET payload_score = ?
WHERE id = ? AND owner_id = ?;

-- name: delete_item
DELETE FROM items
WHERE id = ? AND owner_id = ?;
