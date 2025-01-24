from src.shared.redis.connection_factory import get_connection
from src.shared.pubsub.subscriber import Subscriber, AsyncCallbackType


class RedisSubscriber(Subscriber):
    def __init__(self):
        self.connection = get_connection()

    async def subscribe(self, subscription: str, process: AsyncCallbackType) -> None:
        pubsub = self.connection.pubsub()

        await pubsub.subscribe(subscription)

        async for message in pubsub.listen():
            if message["type"] == "message" and message["channel"] == subscription:
                await process(message["data"])
