import os

from src.users.use_cases.user_query import UserQueryHandler
from src.users.infrastructure.persistence.postgres.postgres_user_repository import (
    PostgresUserRepository,
)
from src.expenses.use_cases.register_user_expense import (
    RegisterUserExpense,
    RegisterUserExpenseRequest,
)
from src.expenses.use_cases.services.expense_details_from_message import (
    GetExpenseDetails,
)
from src.expenses.infrastructure.persistence.postgres.postgres_expense_repository import (
    PostgresExpenseRepository,
)
from src.expenses.infrastructure.persistence.postgres.postgres_message_process_repository import (
    PostgresMessageProcessRepository,
)
from src.shared.postgres.connection import get_connection_pool
from src.shared.llm.impl.langchain_coherence_llm import LangChainCohereTextGenerator
from src.shared.llm.impl.langchain_coherence_llm import LangChainCohereTextGenerator

import json
from src.shared.pubsub.subscriber import Subscriber
from src.shared.pubsub.publisher import Publisher
from src.shared.pubsub.impl.redis_subscriber import RedisSubscriber
from src.shared.pubsub.impl.redis_publisher import RedisPublisher
from src.shared.logging.log import Logger


INBOUND_MSG_SUB = os.getenv("INBOUND_MSG_SUB")
OUTBOUND_MSG_SUB = os.getenv("OUTBOUND_MSG_SUB")

logger = Logger(__name__)


class InboundMessageExpenseSubscriber:
    def __init__(
        self,
        publisher: Publisher,
        subscriber: Subscriber,
        register_expense: RegisterUserExpense,
    ):
        self.publisher = publisher
        self.subscriber = subscriber
        self.register_expense = register_expense

    async def run(self) -> None:
        await self.subscriber.subscribe(INBOUND_MSG_SUB, self.__message_handler)

    async def __message_handler(self, message: str) -> None:
        logger.info(f"Message received {message}")

        message_dict = json.loads(message)

        chat_id = message_dict.get("chat_id")
        message = message_dict.get("message")
        message_id = message_dict.get("message_id")
        user_external_id = message_dict.get("user_external_id")

        request = RegisterUserExpenseRequest(
            message=message, message_id=message_id, user_external_id=user_external_id
        )

        expense = await self.register_expense.from_message(request=request)

        if expense:
            await self.publisher.publish(
                OUTBOUND_MSG_SUB,
                data={
                    "chatId": chat_id,
                    "message": f"{expense.details.category.name} expense added ✅",
                },
            )


def inboundMessageProcessor():
    db_pool = get_connection_pool()
    user_repository = PostgresUserRepository(db_pool)
    user_query_handler = UserQueryHandler(user_repository)
    expenses_repository = PostgresExpenseRepository(db_pool)
    expense_details_service = GetExpenseDetails(LangChainCohereTextGenerator())
    messages_repository = PostgresMessageProcessRepository(db_pool)

    return InboundMessageExpenseSubscriber(
        subscriber=RedisSubscriber(),
        publisher=RedisPublisher(),
        register_expense=RegisterUserExpense(
            users=user_query_handler,
            expenses=expenses_repository,
            get_expense_details=expense_details_service,
            messages=messages_repository,
        ),
    )
