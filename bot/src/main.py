from fastapi import FastAPI, Depends
from pydantic import BaseModel

from contextlib import asynccontextmanager


from src.shared.postgres.connection import init_db, close_db, get_connection_pool
from src.expenses.domain.expense import NewExpense
from src.expenses.infrastructure.persistence.postgres.postgres_expense_repository import (
    PostgresExpenseRepository,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)


class ExpenseRequest(BaseModel):
    message: str
    user_external_id: str


expense = NewExpense(user_id=1, amount=100, category="Food", description="Pizza")


def get_repo(db_pool=Depends(get_connection_pool)):
    return PostgresExpenseRepository(db_pool)


@app.post("/process")
async def process_expense(request: ExpenseRequest):
    return


@app.get("/process")
async def get_exp(request: ExpenseRequest, repo=Depends(get_repo)):
    return await repo.add(expense)
