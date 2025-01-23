import asyncpg
from asyncpg import Pool

import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

db_pool = None


async def init_db():
    global db_pool
    db_pool = await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        min_size=1,
        max_size=10,
    )
    print("✅ Database connected successfully!")


async def close_db():
    global db_pool
    if db_pool:
        await db_pool.close()
        print("🔌 Database connection closed")


async def get_connection_pool() -> Pool:
    if db_pool is None:
        raise Exception("Database pool is not initialized")

    return db_pool
