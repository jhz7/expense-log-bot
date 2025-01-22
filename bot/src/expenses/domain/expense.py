from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal


class ExpenseCategory(Enum):
    Housing = "Housing"
    Transportation = "Transportation"
    Food = "Food"
    Utilities = "Utilities"
    Insurance = "Insurance"
    Medical_Healthcare = "Medical/Healthcare"
    Savings = "Savings"
    Debt = "Debt"
    Education = "Education"
    Entertainment = "Entertainment"
    Other = "Other"


@dataclass
class ExpenseDetails:
    description: str
    amount: Decimal
    category: ExpenseCategory


@dataclass
class NewExpense:
    user_id: int
    details: ExpenseDetails
    at: datetime = datetime.now()
