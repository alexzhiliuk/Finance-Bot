import aiosqlite
from datetime import datetime

DB_PATH = "finance.db"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                amount      REAL    NOT NULL,
                category    TEXT    NOT NULL,
                description TEXT,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def add_expense(
    user_id: int,
    amount: float,
    category: str,
    description: str | None,
) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO expenses (user_id, amount, category, description) VALUES (?, ?, ?, ?)",
            (user_id, amount, category, description),
        )
        await db.commit()
        return cursor.lastrowid


async def get_monthly_expenses(user_id: int, year: int, month: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """
            SELECT id, amount, category, description, created_at
            FROM expenses
            WHERE user_id = ?
              AND strftime('%Y', created_at) = ?
              AND strftime('%m', created_at) = ?
            ORDER BY created_at DESC
            """,
            (user_id, str(year), f"{month:02d}"),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_recent_expenses(user_id: int, limit: int = 10) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """
            SELECT id, amount, category, description, created_at
            FROM expenses
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def delete_expense(expense_id: int, user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM expenses WHERE id = ? AND user_id = ?",
            (expense_id, user_id),
        )
        await db.commit()
        return cursor.rowcount > 0
