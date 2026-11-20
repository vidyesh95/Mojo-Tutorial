# backend/app/main.py
import os
import subprocess
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.health import router as health_router
from backend.app.api.items import router as items_router
from backend.app.auth.router import router as auth_router
from backend.app.db.migrator import run_migrations


def ensure_mojo_extension_compiled():
    """Ensures backend/app/mojo_core.so is compiled from backend/mojo_core/compute.mojo."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mojo_src = os.path.join(base_dir, "mojo_core", "compute.mojo")
    so_dest = os.path.join(base_dir, "app", "mojo_core.so")

    if not os.path.exists(so_dest):
        print(f"Compiling Mojo native extension: {mojo_src} -> {so_dest}...")
        venv_bin = os.path.dirname(sys.executable)
        mojo_bin = os.path.join(venv_bin, "mojo")
        if not os.path.exists(mojo_bin):
            mojo_bin = "mojo"

        subprocess.run(
            [mojo_bin, "build", "--emit", "shared-lib", mojo_src, "-o", so_dest], check=True
        )
        print("Mojo extension compiled successfully!")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle initialization: runs database migrations and verifies Mojo shared library."""
    # Run SQLite migrations
    await run_migrations()
    # Verify/compile Mojo extension
    ensure_mojo_extension_compiled()
    yield


openapi_tags = [
    {
        "name": "Health & Diagnostics",
        "description": "Liveness and readiness probes verifying database pool health and native Mojo shared library status.",
    },
    {
        "name": "Better Auth",
        "description": "Authentication endpoints compatible with Better Auth: Argon2id password hashing, session rotation, and signed HttpOnly cookies.",
    },
    {
        "name": "Domain Items & Mojo Compute",
        "description": "Protected domain CRUD operations and high-performance SIMD batch calculations executed natively by compiled Mojo code.",
    },
]

app = FastAPI(
    title="Mojo + FastAPI Production Backend",
    description="""
## Modern Mojo 🔥 + FastAPI + SQLx-Style SQLite + Better Auth

A high-performance backend architecture combining:
- **Systems Mojo**: Compiled native `.so` CPython extensions running hardware SIMD vector operations.
- **FastAPI**: Async ASGI HTTP routing, dependency injection, and automatic interactive documentation.
- **SQLx-Style SQLite**: Raw parameterized SQL queries, explicit sequential migrations, and pre-flight query validation.
- **Better Auth**: 4-table relational schema (`user`, `session`, `account`, `verification`) with Argon2id password security and HMAC-SHA256 signed session cookies.
    """,
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=openapi_tags,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration allowing credentials for session cookies
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(items_router)
