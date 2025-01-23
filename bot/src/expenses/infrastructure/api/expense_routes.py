from pydantic import BaseModel
from fastapi import APIRouter, Depends

from src.users.use_cases.user_query import UserQueryHandler
from src.users.infrastructure.persistence.postgres.postgres_user_repository import (
    PostgresUserRepository,
)

from src.expenses.use_cases.register_user_expense import (
    RegisterUserExpense,
    RegisterUserExpenseRequest,
)
from src.expenses.use_cases.services.expense_details_from_message import (
    GetExpenseDetails,
)
from src.expenses.infrastructure.persistence.postgres.postgres_expense_repository import (
    PostgresExpenseRepository,
)
from src.expenses.infrastructure.persistence.postgres.postgres_message_process_repository import (
    PostgresMessageProcessRepository,
)

from src.shared.postgres.connection import get_connection_pool
from src.shared.llm.impl.langchain_coherence_llm import LangChainCohereTextGenerator


def get_user_query_handler(db_pool=Depends(get_connection_pool)):
    user_repository = PostgresUserRepository(db_pool)
    user_query_handler = UserQueryHandler(user_repository)

    return user_query_handler


def get_expenses_repository(db_pool=Depends(get_connection_pool)):
    expenses_repository = PostgresExpenseRepository(db_pool)
    return expenses_repository


def get_expenses_details_service(llm=Depends(LangChainCohereTextGenerator)):
    expenses_details_service = GetExpenseDetails(llm)
    return expenses_details_service


def get_messages_repository(db_pool=Depends(get_connection_pool)):
    messages_repository = PostgresMessageProcessRepository(db_pool)
    return messages_repository


router = APIRouter()


class ExpenseLogRequest(BaseModel):
    message: str
    user_external_id: str


@router.post("/expenses")
async def register_expense(
    request: ExpenseLogRequest,
    user_query=Depends(get_user_query_handler),
    expenses_repository=Depends(get_expenses_repository),
    messages_repository=Depends(get_messages_repository),
    expense_details_service=Depends(get_expenses_details_service),
):
    message = RegisterUserExpenseRequest(
        message=request.message, user_external_id=request.user_external_id
    )
    service = RegisterUserExpense(
        users=user_query,
        expenses=expenses_repository,
        get_expense_details=expense_details_service,
        messages=messages_repository,
    )

    expense = await service.from_message(message)

    if not expense:
        return {"message": None}

    return {"message": f"{expense.details.category.name} expense added ✅"}
