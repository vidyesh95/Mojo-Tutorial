# backend/app/db/verifier.py
"""
SQLx-Style Pre-Flight Query Verifier for SQLite.
Parses every named query in backend/app/db/queries/*.sql and runs
EXPLAIN QUERY PLAN against the live SQLite schema to catch broken column names,
table names, and invalid SQL syntax before deployment or CI.
"""
import asyncio
import os
import re
import aiosqlite
from backend.app.config import settings
from backend.app.db.migrator import run_migrations

def parse_queries(sql_content: str) -> dict[str, str]:
    """Extracts named queries defined with '-- name: <query_name>' annotations."""
    queries = {}
    current_name = None
    current_lines = []

    for line in sql_content.splitlines():
        name_match = re.match(r"^--\s*name:\s*([a-zA-Z0-9_]+)", line)
        if name_match:
            if current_name and current_lines:
                queries[current_name] = "\n".join(current_lines).strip()
                current_lines = []
            current_name = name_match.group(1)
        elif current_name:
            if not line.startswith("--"):
                current_lines.append(line)

    if current_name and current_lines:
        queries[current_name] = "\n".join(current_lines).strip()

    return queries

async def verify_queries(db_path: str = settings.DATABASE_PATH):
    # Ensure database migrations are current first
    await run_migrations(db_path)

    queries_dir = os.path.join(os.path.dirname(__file__), "queries")
    sql_files = sorted([f for f in os.listdir(queries_dir) if f.endswith(".sql")])

    print("Verifying SQL queries against live schema...")
    verified_count = 0

    async with aiosqlite.connect(db_path) as conn:
        for filename in sql_files:
            filepath = os.path.join(queries_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            named_queries = parse_queries(content)
            print(f"  Found {len(named_queries)} named queries in {filename}:")

            for name, sql in named_queries.items():
                if not sql:
                    continue
                # Count '?' positional parameters
                param_count = sql.count("?")
                dummy_params = [None] * param_count

                try:
                    # SQLite's EXPLAIN checks table existence, column names, and query plans
                    explain_sql = f"EXPLAIN {sql}"
                    await conn.execute(explain_sql, dummy_params)
                    print(f"    ✓ {name}")
                    verified_count += 1
                except Exception as e:
                    raise RuntimeError(f"SQLx Verification Failed for query '{name}' in {filename}:\n{sql}\nError: {e}") from e

    print(f"SUCCESS: All {verified_count} raw SQL queries verified against SQLite schema!")

if __name__ == "__main__":
    asyncio.run(verify_queries())
