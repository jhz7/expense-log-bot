from fastapi import FastAPI, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
from datetime import datetime

from contextlib import asynccontextmanager

from langchain_community.llms import Cohere
from langchain_core.prompts import PromptTemplate

from src.shared.postgres.connection import init_db, close_db, get_connection_pool
from src.expenses.domain.expense import NewExpense
from src.expenses.infrastructure.persistence.postgres.postgres_expense_repository import PostgresExpenseRepository

load_dotenv()


cohere_api_key = os.environ.get("COHERE_API_KEY")
model = Cohere(cohere_api_key=cohere_api_key, max_tokens=256, temperature=0.75)
prompt = PromptTemplate(
    input_variables=["expense_text"],
    template="""
    You are a financial assistant that categorizes expenses and extracts details.
    Given an expense description, extract the following:

    1. The name or description of the expense (e.g., "Pizza", "Taxi").
    2. The amount of money spent (e.g., "20 bucks", "50 USD").
    3. The category of the expense from the following list: Housing, Transportation, Food, Utilities, Insurance, Medical/Healthcare, Savings, Debt, Education, Entertainment, and Other.

    Expense description: "{expense_text}"

    Provide your response in the following format:
    {{
        description: [Expense description],
        amount: [Amount spent],
        category: [Category],
    }}

    Example:
    Expense description: "Pizza 20 bucks"
    Response: 
    {{
        description: Pizza,
        amount: 20,
        category: Food
    }}
    """,
)
chain = prompt | model


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await init_db()
    yield
    # Clean up the ML models and release the resources
    await close_db()


app = FastAPI(lifespan=lifespan)


class ExpenseRequest(BaseModel):
    user_id: int
    message: str

expense = NewExpense(user=1, amount=100, category="Food", description="Pizza")

def get_repo(db_pool=Depends(get_connection_pool)):
    return PostgresExpenseRepository(db_pool)

@app.post("/process")
async def process_expense(request: ExpenseRequest):
    msg = chain.invoke({"expense_text": request.message})
    print(json.loads(msg))

    return {"message": f"Received: {request.message}", "generated": msg}

@app.get("/process")
async def get_exp(request: ExpenseRequest, repo=Depends(get_repo)):

    return await repo.add(expense)
