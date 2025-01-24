import json
from dataclasses import asdict

from asyncpg import Pool
from src.expenses.domain.message_process import (
    MassageProcessRepository,
    ProcessedMassage,
)
from src.shared.errors.technical import TechnicalError
from src.shared.logging.log import Logger

logger = Logger(__name__)


class PostgresMessageProcessRepository(MassageProcessRepository):
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def exists(self, message_id: str) -> bool:
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT count(id) FROM processed_messages WHERE id = $1",
                    message_id,
                )

                return bool(rows) and rows[0]["count"] > 0
        except Exception as e:
            error = TechnicalError(
                code="MassageProcessRepositoryError",
                message=f"Fail checking if a message has been processed: message_id={message_id}",
                attributes={"message_id": message_id},
                cause=e,
            )

            logger.error(error)

            raise error from e

    async def add(self, message_process: ProcessedMassage) -> None:
        as_dict_result = asdict(message_process.result)
        as_dict_result["kind"] = message_process.result.kind.value
        try:
            async with self.db_pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(
                        "INSERT INTO processed_messages (id, user_id, message_content, result, added_at) VALUES ($1, $2, $3, $4, $5)",
                        message_process.message.id,
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
