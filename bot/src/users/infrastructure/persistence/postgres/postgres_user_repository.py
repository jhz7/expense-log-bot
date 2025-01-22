from asyncpg import Pool
from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository
from src.shared.errors.technical import TechnicalError
from src.shared.errors.application import NotFoundError
from src.shared.logging.log import Logger

logger = Logger(__name__)


class PostgresUserRepository(UserRepository):
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def get(self, user_id: int) -> User:
        found_user = await self.find(user_id)

        if found_user:
            return found_user

        error = NotFoundError(
            resource="User",
            attributes={"user_id": user_id},
        )

        logger.error(error)

        raise error

    async def find(self, user_id: int) -> User | None:
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT id, telegram_id FROM users WHERE telegram_id = $1", user_id
                )

                if not rows or len(rows) == 0:
                    return None

                row = rows[0]

                return User(id=row["id"], telegram_id=row["telegram_id"])
        except Exception as e:
            error = TechnicalError(
                code="UserRepositoryError",
                message=f"Fail finding the user {user_id}",
                attributes={"user_id": user_id},
                cause=e,
            )

            logger.error(error)

            raise error from e
