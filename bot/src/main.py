from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.expenses.infrastructure.api.expense_routes import router as expenses_router
from src.shared.postgres.connection import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(expenses_router)
