from enum import Enum
from datetime import datetime
from dataclasses import dataclass


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
    amount: float
    category: ExpenseCategory


class NewExpense:
    def __init__(
        self,
        user_id: int,
        details: ExpenseDetails,
        at: datetime = datetime.now(),
    ):
        self.user_id = user_id
        self.details = details
        self.at = at

    def __str__(self):
        return f"NewExpense(description={self.description}, amount={self.amount}, category={self.category})"

    def __repr__(self):
        return str(self)
