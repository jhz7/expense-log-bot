from dataclasses import dataclass
from src.users.use_cases.user_query import UserQueryHandler
from src.expenses.domain.expense import NewExpense, ExpenseDetails
from src.expenses.domain.expense_repository import ExpenseRepository
from src.expenses.use_cases.services.expense_details_from_message import (
    GetExpenseDetails,
)
from src.expenses.domain.message_process import (
    Message,
    MassageProcess,
    MassageProcessRepository,
)


@dataclass
class RegisterUserExpenseRequest:
    message: str
    user_external_id: str


class RegisterUserExpense:
    def __init__(
        self,
        users: UserQueryHandler,
        expenses: ExpenseRepository,
        get_expense_details: GetExpenseDetails,
        messages: MassageProcessRepository,
    ):
        self.users = users
        self.expenses = expenses
        self.messages = messages
        self.get_expense_details = get_expense_details

    async def from_message(
        self, request: RegisterUserExpenseRequest
    ) -> NewExpense | None:
        found_user = await self.users.get(request.user_external_id)

        message = Message(user_id=found_user.id, content=request.message)

        try:
            expense_details_or_generated_text = (
                await self.get_expense_details.from_message(message=message)
            )

            if not isinstance(expense_details_or_generated_text, ExpenseDetails):
                generated_text = expense_details_or_generated_text
                message_process_result = MassageProcess.failed(
                    message=message,
                    error=f"No parsed message: generated_text {generated_text}",
                )

                return None

            expense_details = expense_details_or_generated_text
            new_expense = NewExpense(
                user_id=found_user.id,
                details=expense_details,
            )

            expense_id = await self.expenses.add(new_expense)

            message_process_result = MassageProcess.succeed(
                message=message, expense_id=expense_id
            )

            return new_expense
        except Exception as e:
            message_process_result = MassageProcess.failed(
                message=message, error=str(e)
            )

            return None
        finally:
            await self.messages.add(message_process_result)
