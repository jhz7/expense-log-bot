from asyncpg import Pool
from src.expenses.domain.expense import NewExpense
from src.expenses.domain.expense_repository import ExpenseRepository
from src.shared.errors.technical import TechnicalError
from src.shared.logging.log import Logger

logger = Logger(__name__)


class PostgresExpenseRepository(ExpenseRepository):
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def add(self, expense: NewExpense) -> int:
        try:
            async with self.db_pool.acquire() as connection:
                async with connection.transaction():
                    inserted_id = await connection.fetchval(
                        "INSERT INTO expenses (user_id, amount, category, description, added_at) VALUES ($1, $2, $3, $4, $5) RETURNING id",
                        expense.user_id,
                        str(expense.details.amount),
                        expense.details.category.name,
                        expense.details.description,
                        expense.at,
                    )

                    return inserted_id
        except Exception as e:
            error = TechnicalError(
                code="ExpenseRepositoryError",
                message=f"Fail adding a new expense for user {expense.user_id}",
                attributes=expense.__dict__,
                cause=e,
            )

            logger.error(error)

            raise error from e
