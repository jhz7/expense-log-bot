import json
import re
from dataclasses import dataclass
from decimal import Decimal

from src.expenses.domain.expense import ExpenseDetails, ExpenseCategory
from src.shared.llm.llm import LLM
from src.shared.logging.log import Logger
from src.shared.errors.application import ApplicationError


@dataclass
class Message:
    content: str
    user_external_id: str


prompt = """
    You are a financial assistant that categorizes expenses and extracts details.
    Given an expense description, extract the following:

    1. The name or description of the expense (e.g., "Pizza", "Taxi").
    2. The amount of money spent (e.g., 100) always do an effort to conver to USD dollars or return the numric value by default.
    3. The category of the expense from the following list: Housing, Transportation, Food, Utilities, Insurance, Medical/Healthcare, Savings, Debt, Education, Entertainment, and Other.

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

    async def from_message(self, message: Message) -> ExpenseDetails | None:
        generated_data = await self.llm.generate(
            prompt, input={"expense_text": message.content}
        )

        try:
            json_match = re.search(r"({.*?})", generated_data, re.DOTALL)
            parsed_data = json.loads(json_match.group(0))
        except Exception as e:
            logger.error(e)
            raise ValueError(f"Error parsing generated data {generated_data}") from e

        expected_keys = {"amount", "description", "category"}

        if not expected_keys.issubset(parsed_data.keys()):
            return None

        try:
            solved = parsed_data.get("solved")

            if not isinstance(solved, bool):
                raise ValueError(f"Invalid 'solved' value: {solved}")

            if not solved:
                return None

            amount = parsed_data.get("amount")
            category = parsed_data.get("category")
            description = parsed_data.get("description")

            if not isinstance(amount, (int, float, str)):
                raise ValueError(f"Invalid 'amount' value: {amount}")
            amount = Decimal(amount)

            if not isinstance(description, str) or not description.strip():
                raise ValueError(f"Invalid 'description' value: {description}")

            if not isinstance(category, str) or not ExpenseCategory(category.strip()):
                raise ValueError(f"Invalid 'category' value: {category}")
            category = ExpenseCategory(category)

            return ExpenseDetails(
                amount=amount, description=description, category=category
            )
        except ValueError as e:
            error = ApplicationError(
                code="ExpenseDetailsError",
                message="Error parsing generated data",
                attributes=parsed_data,
            )

            logger.error(error)

            raise error from e
