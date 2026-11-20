# backend/app/db/pool.py
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TypeVar

import aiosqlite
from pydantic import BaseModel

from backend.app.config import settings

T = TypeVar("T", bound=BaseModel)


@asynccontextmanager
async def get_connection() -> AsyncGenerator[aiosqlite.Connection]:
    """Provides an aiosqlite connection with WAL mode and foreign keys enabled."""
    conn = await aiosqlite.connect(settings.DATABASE_PATH)
    conn.row_factory = aiosqlite.Row
    await conn.execute("PRAGMA foreign_keys = ON;")
    await conn.execute("PRAGMA journal_mode = WAL;")
    try:
        yield conn
    finally:
        await conn.close()


async def fetch_one[T: BaseModel](query: str, model: type[T], params: tuple = ()) -> T | None:
    """Executes a query and maps the first record directly into a Pydantic model."""
    async with get_connection() as conn, conn.execute(query, params) as cursor:
        row = await cursor.fetchone()
        if row is None:
            return None
        return model.model_validate(dict(row))


async def fetch_all[T: BaseModel](query: str, model: type[T], params: tuple = ()) -> list[T]:
    """Executes a query and maps all records into a list of Pydantic models."""
    async with get_connection() as conn, conn.execute(query, params) as cursor:
        rows = await cursor.fetchall()
        return [model.model_validate(dict(row)) for row in rows]


async def execute(query: str, params: tuple = ()) -> int:
    """Executes a parameterized mutation query and commits changes."""
    async with get_connection() as conn:
        cursor = await conn.execute(query, params)
        await conn.commit()
        return cursor.rowcount
