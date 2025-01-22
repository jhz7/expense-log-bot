from src.users.use_cases.user_query import UserQuery
from src.expenses.domain.expense import NewExpense
from src.expenses.domain.expense_repository import ExpenseRepository
from src.expenses.use_cases.services.expense_details_from_message import (
    GetExpenseDetails,
    Message,
)


class RegisterUserExpense:
    def __init__(
        self,
        users: UserQuery,
        expenses: ExpenseRepository,
        get_expense_details: GetExpenseDetails,
    ):
        self.users = users
        self.expenses = expenses
        self.get_expense_details = get_expense_details

    async def from_message(self, message: Message):
        found_user = await self.users.get(message.user_id)

        expense_details = await self.get_expense_details.from_message(message)

        if expense_details:
            await self.expenses.add(
                NewExpense(
                    user_id=found_user.id,
                    details=expense_details,
                )
            )
