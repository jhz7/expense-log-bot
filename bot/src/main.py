from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json

from contextlib import asynccontextmanager

from langchain_community.llms import Cohere
from langchain_core.prompts import PromptTemplate

import asyncio
from src.database import init_db, close_db, get_whitelisted_users

load_dotenv()


cohere_api_key=os.environ.get("COHERE_API_KEY")
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
    """
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


# @app.on_event("startup")
# async def startup_event():
#     await init_db()

# @app.on_event("shutdown")
# async def shutdown_event():
#     await close_db()
    
@app.get("/process")
async def process_expense(request: ExpenseRequest):
    # msg = chain.invoke({"expense_text": request.message})
    # print(json.loads(msg))

    # return {"message": f"Received: {request.message}", "generated": msg}
    return await get_whitelisted_users()
