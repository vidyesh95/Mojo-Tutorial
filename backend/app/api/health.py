# backend/app/api/health.py
import aiosqlite
from fastapi import APIRouter, HTTPException, status

from backend.app.config import settings

router = APIRouter(tags=["Health & Diagnostics"])


def get_mojo_engine_status() -> str:
    """Attempts to import the compiled native Mojo extension."""
    try:
        from backend.app import mojo_core

        return mojo_core.ping()
    except Exception as e:
        return f"unavailable: {e}"


@router.get("/health")
async def health_check():
    """Liveness probe returning application metadata."""
    return {
        "status": "healthy",
        "service": "mojo-fastapi-backend",
        "environment": settings.ENVIRONMENT,
    }


@router.get("/ready")
async def readiness_check():
    """Readiness probe checking SQLite database connectivity and native Mojo extension."""
    db_ok = False
    try:
        async with (
            aiosqlite.connect(settings.DATABASE_PATH) as conn,
            conn.execute("SELECT 1") as cursor,
        ):
            row = await cursor.fetchone()
            db_ok = row is not None and row[0] == 1
    except Exception:
        db_ok = False

    mojo_status = get_mojo_engine_status()
    mojo_ok = "online" in mojo_status

    if not db_ok:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"database": "down", "mojo_core": mojo_status},
        )

    return {
        "status": "ready",
        "database": "connected",
        "mojo_core": mojo_status,
        "simd_acceleration": mojo_ok,
    }
