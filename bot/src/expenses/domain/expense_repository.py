from abc import ABC, abstractmethod
from src.expenses.domain.expense import NewExpense


class ExpenseRepository(ABC):
    @abstractmethod
    async def add(self, expense: NewExpense) -> None:
        pass
