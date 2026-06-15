from app.domain.entities.event import UserEvent
from app.domain.repositories.event_repository import EventRepository


class RecordEventUseCase:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    def execute(self, event: UserEvent) -> UserEvent:
        return self.repository.add(event)
