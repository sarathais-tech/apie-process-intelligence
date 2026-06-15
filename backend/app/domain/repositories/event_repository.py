from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.event import UserEvent


class EventRepository(ABC):
    @abstractmethod
    def add(self, event: UserEvent) -> UserEvent:
        raise NotImplementedError

    @abstractmethod
    def list(self, limit: int = 100, offset: int = 0) -> list[UserEvent]:
        raise NotImplementedError

    @abstractmethod
    def get(self, event_id: UUID) -> UserEvent | None:
        raise NotImplementedError
