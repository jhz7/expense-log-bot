import datetime
# from dataclasses import dataclass


class NewExpense:
    def __init__(
        self,
        user: int,
        amount: float,
        category: str,
        description: str,
        at: datetime = datetime.now(),
    ):
        self.user = user
        self.amount = amount
        self.category = category
        self.description = description
        self.at = at

    def __str__(self):
        return f"NewExpense(description={self.description}, amount={self.amount}, category={self.category})"

    def __repr__(self):
        return str(self)
