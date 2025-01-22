import json
from dataclasses import asdict

from asyncpg import Pool
from src.expenses.domain.message_process import MassageProcessRepository, MassageProcess
from src.shared.errors.technical import TechnicalError
from src.shared.logging.log import Logger

logger = Logger(__name__)


class PostgresMessageProcessRepository(MassageProcessRepository):
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def add(self, message_process: MassageProcess) -> None:
        as_dict_result = asdict(message_process.result)
        as_dict_result["kind"] = message_process.result.kind.value
        try:
            async with self.db_pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(
                        "INSERT INTO message_processing (user_id, message_content, result, added_at) VALUES ($1, $2, $3, $4)",
                        message_process.message.user_id,
                        message_process.message.content,
                        json.dumps(as_dict_result),
                        message_process.at,
                    )
        except Exception as e:
            error = TechnicalError(
                code="MassageProcessRepositoryError",
                message=f"Fail adding a new message processing log for user {message_process.message.user_id}",
                attributes=asdict(message_process),
                cause=e,
            )

            logger.error(error)

            raise error from e
