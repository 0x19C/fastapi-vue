import os
import asyncio
import aiomysql

async def create_database_if_not_exists():
    db_config = {
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "port": int(os.environ.get("DB_PORT", "3306")),
    }
    database_name = os.environ.get("DB_NAME", "corpy_test")

    # Connect to the MySQL server
    conn = await aiomysql.connect(**db_config)
    async with conn.cursor() as cursor:
        await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    await conn.ensure_closed()

# Call this function at the start of your app
if __name__ == "__main__":
    asyncio.run(create_database_if_not_exists())
