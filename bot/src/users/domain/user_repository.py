from abc import ABC, abstractmethod
from src.users.domain import User


class UserRepository(ABC):
    @abstractmethod
    async def get(self, user_id: int) -> User:
        pass
    
    @abstractmethod
    async def find(self, user_id: int) -> User | None:
        pass
