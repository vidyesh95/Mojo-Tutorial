# backend/tests/test_sql_queries.py
import pytest

from backend.app.db.verifier import verify_queries


@pytest.mark.asyncio
async def test_all_sql_queries_pass_sqlite_verifier(tmp_path):
    """
    SQLx-style verification test: validates all raw .sql queries in
    backend/app/db/queries/*.sql against a clean SQLite schema.
    """
    test_db = str(tmp_path / "verify_test.db")
    # Should execute without raising any exceptions
    await verify_queries(test_db)
