# backend/tests/test_compute_api.py
import asyncio
import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.config import settings
from backend.app.db.migrator import run_migrations
from backend.app.main import app

@pytest.fixture(autouse=True)
def setup_test_environment(tmp_path, monkeypatch):
    test_db = str(tmp_path / "api_test.db")
    monkeypatch.setattr("backend.app.config.settings.DATABASE_PATH", test_db)
    asyncio.run(run_migrations(test_db))

@pytest.mark.asyncio
async def test_health_and_readiness_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Liveness check
        res = await client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"

        # 2. Readiness check
        ready_res = await client.get("/ready")
        assert ready_res.status_code == 200
        data = ready_res.json()
        assert data["database"] == "connected"
        assert "mojo-1.2-engine-online" in data["mojo_core"]

@pytest.mark.asyncio
async def test_full_items_and_mojo_compute_workflow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Sign up user
        signup_res = await client.post("/api/auth/sign-up/email", json={
            "name": "Backend Tester",
            "email": "backend_dev@example.com",
            "password": "Password12345!"
        })
        assert signup_res.status_code == 201
        assert settings.SESSION_COOKIE_NAME in signup_res.cookies

        # 2. Create items via raw SQL
        item_res = await client.post("/api/items", json={
            "title": "Production Server Risk Metric",
            "initial_score": 10.0
        })
        assert item_res.status_code == 201
        item = item_res.json()
        assert item["title"] == "Production Server Risk Metric"
        assert item["payload_score"] == 10.0

        # 3. List items
        list_res = await client.get("/api/items")
        assert list_res.status_code == 200
        items = list_res.json()
        assert len(items) == 1

        # 4. Invoke high-performance Mojo SIMD batch score endpoint
        score_res = await client.post("/api/compute/batch-score", json={
            "custom_features": [1.0, 2.0, 3.0, 4.0, 5.0]
        })
        assert score_res.status_code == 200
        score_data = score_res.json()
        assert score_data["processed_count"] == 5
        assert score_data["engine"] == "mojo-1.2-simd"
        assert len(score_data["scores"]) == 5
        assert score_data["execution_time_ms"] >= 0.0

        # Unauthenticated request without cookies should be rejected
        anon_client = AsyncClient(transport=transport, base_url="http://test")
        unauth_res = await anon_client.get("/api/items")
        assert unauth_res.status_code == 401
