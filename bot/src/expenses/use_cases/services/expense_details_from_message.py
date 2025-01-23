import json
import re
from decimal import Decimal

from src.expenses.domain.expense import ExpenseDetails, ExpenseCategory
from src.expenses.domain.message_process import Message
from src.shared.llm.llm import LLM
from src.shared.logging.log import Logger
from src.shared.errors.application import ApplicationError


prompt = """
    You are a financial assistant that categorizes expenses and extracts details.
    Given an expense description, extract the following:

    1. The name or description of the expense (e.g., "Pizza", "Taxi").
    2. The amount of money spent (e.g., 100) always do an effort to conver to USD dollars or return the numeric value by default.
    3. The category of the expense restricted to the following: Housing, Transportation, Food, Utilities, Insurance, Medical/Healthcare, Savings, Debt, Education, Entertainment, Other.

    Expense description: "{expense_text}"

    Provide your response in the following format:
    {{
        solved: [true or false],
        description: [Expense description],
        amount: [Amount spent],
        category: [Category],
    }}

    Example:
    Expense description: "Pizza 20 bucks" or "Pizza 20"
    Response: 
    {{
        solved: true,
        description: Pizza,
        amount: 20,
        category: Food
    }}

    Note: If the expense description is not clear and you can not determine the full expense details, you must return the not solved response {{
        solved: false
    }}. Limit your response to the JSON samples provided and nothing else.
"""

logger = Logger(__name__)


class GetExpenseDetails:
    def __init__(self, llm: LLM):
        self.llm = llm

    async def from_message(self, message: Message) -> ExpenseDetails | str:
        generated_data = await self.llm.generate(
            prompt, input={"expense_text": message.content}
        )

        try:
            parsed_data = self.__generated_text_to_dict(text=generated_data)
            solved = parsed_data.get("solved")

            if not isinstance(solved, bool):
                raise ValueError(f"Invalid 'solved' value: {solved}")

            if not solved:
                return generated_data

            expected_keys = {"amount", "description", "category"}

            if not expected_keys.issubset(parsed_data.keys()):
                return generated_data

            expense_details = self.__map_as_expense_details(parsed_data=parsed_data)

            return expense_details
        except Exception as e:
            error = ApplicationError(
                code="ExpenseDetailsError",
                message=str(e),
                attributes={"text": generated_data},
            )

            logger.error(error)

            raise error from e

    def __generated_text_to_dict(self, text: str) -> dict:
        try:
            json_match = re.search(r"({.*?})", text, re.DOTALL)
            parsed_data = json.loads(json_match.group(0))

            return parsed_data
        except Exception as e:
            logger.error(e)
            raise ValueError(f"Error parsing generated data {text} {repr(e)}") from e

    def __map_as_expense_details(self, parsed_data: dict) -> ExpenseDetails:
        try:
            amount = Decimal(parsed_data.get("amount"))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid amount value: {amount}") from e

        description = parsed_data.get("description")
        if not isinstance(description, str) or not description.strip():
            raise ValueError(f"Invalid description value: {description}")

        try:
            category = ExpenseCategory(parsed_data.get("category"))
        except Exception as e:
            raise ValueError(f"Invalid category value: {category}") from e

        return ExpenseDetails(amount=amount, description=description, category=category)
