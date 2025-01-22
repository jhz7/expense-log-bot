from abc import ABC, abstractmethod
from src.users.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get(self, external_id: str) -> User:
        pass

    @abstractmethod
    async def find(self, external_id: str) -> User | None:
        pass
