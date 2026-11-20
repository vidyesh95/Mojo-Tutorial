# backend/app/db/migrator.py
import asyncio
import os

import aiosqlite

from backend.app.config import settings


async def run_migrations(db_path: str = settings.DATABASE_PATH):
    """
    Applies versioned SQL migrations in sequential order.
    Tracks applied migrations in a _schema_migrations table.
    """
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    migrations_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "migrations"
    )

    print(f"Running migrations on {db_path} from {migrations_dir}...")
    async with aiosqlite.connect(db_path) as conn:
        await conn.execute("PRAGMA foreign_keys = ON;")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS _schema_migrations (
                version TEXT PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await conn.commit()

        # Fetch already applied migration files
        async with conn.execute("SELECT version FROM _schema_migrations") as cursor:
            applied = {row[0] for row in await cursor.fetchall()}

        # Read and apply pending migration files
        migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith(".sql")])
        for filename in migration_files:
            if filename in applied:
                continue

            filepath = os.path.join(migrations_dir, filename)
            print(f"Applying migration: {filename}")
            with open(filepath, encoding="utf-8") as f:
                sql_script = f.read()

            await conn.executescript(sql_script)
            await conn.execute("INSERT INTO _schema_migrations (version) VALUES (?)", (filename,))
            await conn.commit()
            print(f"Successfully applied {filename}")


if __name__ == "__main__":
    asyncio.run(run_migrations())
