#!/usr/bin/env python3
import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All Users:", rows)
            return rows


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("Users older than 40:", rows)
            return rows


async def fetch_concurrently():
    """Run both fetch operations concurrently."""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
