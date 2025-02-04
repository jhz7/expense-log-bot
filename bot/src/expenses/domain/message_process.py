from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from typing import final, Literal
from datetime import datetime


@dataclass
class Message:
    id: str
    user_id: int
    content: str


class MassageProcessResultKind(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class MassageProcessResult(ABC):
    @property
    @abstractmethod
    def kind(self) -> MassageProcessResultKind:
        pass


@dataclass
class MassageProcessSucceed(MassageProcessResult):
    expense_id: int

    @property
    @final
    def kind(self) -> Literal[MassageProcessResultKind.SUCCESS]:
        return MassageProcessResultKind.SUCCESS


@dataclass
class MassageProcessFailed(MassageProcessResult):
    error: str

    @property
    @final
    def kind(self) -> Literal[MassageProcessResultKind.FAILURE]:
        return MassageProcessResultKind.FAILURE


@dataclass
class ProcessedMassage:
    message: Message
    result: MassageProcessResult
    at: datetime = datetime.now()

    @staticmethod
    def succeed(message: Message, expense_id: int) -> "ProcessedMassage":
        return ProcessedMassage(message, MassageProcessSucceed(expense_id))

    @staticmethod
    def failed(message: Message, error: str) -> "ProcessedMassage":
        return ProcessedMassage(message, MassageProcessFailed(error))


class MassageProcessRepository(ABC):
    @abstractmethod
    async def exists(self, message_id: str) -> bool:
        pass

    @abstractmethod
    async def add(self, message_process: ProcessedMassage) -> None:
        pass
