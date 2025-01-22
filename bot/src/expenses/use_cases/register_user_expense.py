from src.users.use_cases.user_query import UserQueryHandler
from src.expenses.domain.expense import NewExpense
from src.expenses.domain.expense_repository import ExpenseRepository
from src.expenses.use_cases.services.expense_details_from_message import (
    GetExpenseDetails,
    Message,
)


class RegisterUserExpense:
    def __init__(
        self,
        users: UserQueryHandler,
        expenses: ExpenseRepository,
        get_expense_details: GetExpenseDetails,
    ):
        self.users = users
        self.expenses = expenses
        self.get_expense_details = get_expense_details

    async def from_message(self, message: Message) -> NewExpense | None:
        found_user = await self.users.get(message.user_external_id)

        expense_details = await self.get_expense_details.from_message(message)
        new_expense = NewExpense(
            user_id=found_user.id,
            details=expense_details,
        )

        if expense_details:
            await self.expenses.add(
                NewExpense(
                    user_id=found_user.id,
                    details=expense_details,
                )
            )

            return new_expense

        return None
