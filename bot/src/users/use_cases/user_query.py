from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository


class UserQuery:
    def __init__(self, users: UserRepository):
        self.__users = users

    async def find(self, external_user_id: str) -> User | None:
        return await self.__users.find(external_user_id)

    async def get(self, external_user_id: str) -> User:
        return await self.__users.get(external_user_id)
