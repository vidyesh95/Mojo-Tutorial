# backend/app/api/items.py
import os
import time
import uuid
from datetime import UTC, datetime

import anyio
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.app.auth.dependencies import CurrentUser
from backend.app.db.pool import execute, fetch_all, fetch_one
from backend.app.db.verifier import parse_queries

router = APIRouter(prefix="/api", tags=["Domain Items & Mojo Compute"])

# Load raw SQL queries from items.sql
queries_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "db", "queries", "items.sql"
)
with open(queries_path, encoding="utf-8") as f:
    ITEMS_SQL = parse_queries(f.read())


class Item(BaseModel):
    id: str
    owner_id: str
    title: str
    payload_score: float
    created_at: str


class CreateItemRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    initial_score: float = Field(default=1.0)


class BatchScoreRequest(BaseModel):
    custom_features: list[float] = Field(default_factory=list)


class BatchScoreResponse(BaseModel):
    processed_count: int
    scores: list[float]
    execution_time_ms: float
    engine: str


def run_mojo_simd_kernel(features: list[float]) -> list[float]:
    """Runs the compiled native Mojo SIMD batch scoring function."""
    from backend.app import mojo_core

    return mojo_core.compute_batch_risk(features)


@router.get("/items", response_model=list[Item])
async def list_items(user: CurrentUser):
    """Lists all items belonging to the authenticated user via parameterized raw SQL."""
    return await fetch_all(ITEMS_SQL["list_user_items"], Item, (user.id,))


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(payload: CreateItemRequest, user: CurrentUser):
    """Creates a new item scoped to the authenticated user."""
    item_id = str(uuid.uuid4())
    now_iso = datetime.now(UTC).isoformat()

    await execute(
        ITEMS_SQL["create_item"], (item_id, user.id, payload.title, payload.initial_score, now_iso)
    )

    created = await fetch_one(ITEMS_SQL["get_item_by_id"], Item, (item_id,))
    if not created:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve created item",
        )
    return created


@router.post("/compute/batch-score", response_model=BatchScoreResponse)
async def batch_score(payload: BatchScoreRequest, user: CurrentUser):
    """
    Protected high-performance endpoint:
    Offloads compute-heavy SIMD scoring to compiled native Mojo code via a worker thread,
    ensuring CPU-bound workloads never block Uvicorn's async event loop.
    """
    # 1. Determine features to score
    features = payload.custom_features
    if not features:
        # Default to scoring user's existing items
        user_items = await fetch_all(ITEMS_SQL["list_user_items"], Item, (user.id,))
        if not user_items:
            features = [1.0, 2.5, 3.8, 4.2, 5.0]
        else:
            features = [item.payload_score for item in user_items]

    # 2. Dispatch to compiled Mojo SIMD kernel asynchronously
    start_time = time.perf_counter()
    scores = await anyio.to_thread.run_sync(run_mojo_simd_kernel, features)
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return BatchScoreResponse(
        processed_count=len(scores),
        scores=scores,
        execution_time_ms=round(elapsed_ms, 3),
        engine="mojo-1.2-simd",
    )
