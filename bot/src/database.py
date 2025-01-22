import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "expenses_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Connection Pool
db_pool = None

async def init_db():
    global db_pool
    db_pool = await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        min_size=1,  # Minimum number of connections
        max_size=10  # Maximum number of connections
    )
    print("✅ Database connected successfully!")

async def close_db():
    global db_pool
    if db_pool:
        await db_pool.close()
        print("🔌 Database connection closed")

async def get_whitelisted_users():
    global db_pool
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, telegram_id FROM users")
        print(rows)
        return {row["telegram_id"] for row in rows}
    
async def add_expense(user_id: int, description: str, amount: float, category: str):
    global db_pool
    async with db_pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO expenses (user_id, description, amount, category, added_at) VALUES ($1, $2, $3, $4, NOW())",
            user_id, description, amount, category
        )