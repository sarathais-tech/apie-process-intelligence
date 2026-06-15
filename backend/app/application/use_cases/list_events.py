from app.domain.entities.event import UserEvent
from app.domain.repositories.event_repository import EventRepository


class ListEventsUseCase:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    def execute(self, limit: int = 100, offset: int = 0) -> list[UserEvent]:
        return self.repository.list(limit=limit, offset=offset)
