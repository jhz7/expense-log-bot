from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository


class FindUser:
    def __init__(self, users: UserRepository):
        self.users = users

    async def execute(self, external_user_id: str) -> User | None:
        return await self.users.find(external_user_id)
