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


app = FastAPI(
    title="Mojo + FastAPI Production Backend",
    description="Full-stack backend combining Systems Mojo SIMD computing, SQLx-style SQLite, and Better Auth.",
    version="1.0.0",
    lifespan=lifespan,
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
