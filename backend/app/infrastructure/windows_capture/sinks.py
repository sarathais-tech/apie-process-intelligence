from abc import ABC, abstractmethod

from app.domain.entities.event import UserEvent


class EventSink(ABC):
    @abstractmethod
    def save(self, event: UserEvent) -> UserEvent:
        raise NotImplementedError


class ApiEventSink(EventSink):
    def __init__(self, api_url: str = "http://localhost:8000/api/v1/events", timeout_seconds: int = 10) -> None:
        self.api_url = api_url
        self.timeout_seconds = timeout_seconds

    def save(self, event: UserEvent) -> UserEvent:
        import requests

        requests.post(
            self.api_url,
            json=event_to_payload(event),
            timeout=self.timeout_seconds,
        ).raise_for_status()
        return event


class PostgresEventSink(EventSink):
    def save(self, event: UserEvent) -> UserEvent:
        from app.infrastructure.database.session import SessionLocal
        from app.infrastructure.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository

        with SessionLocal() as db:
            return SqlAlchemyEventRepository(db).add(event)


class InMemoryEventSink(EventSink):
    def __init__(self) -> None:
        self.events: list[UserEvent] = []

    def save(self, event: UserEvent) -> UserEvent:
        self.events.append(event)
        return event


def event_to_payload(event: UserEvent) -> dict:
    return {
        "event_type": event.event_type.value,
        "source": event.source,
        "user_id": event.user_id,
        "session_id": event.session_id,
        "process_name": event.process_name,
        "window_title": event.window_title,
        "activity": event.activity,
        "metadata": event.metadata,
        "occurred_at": event.occurred_at.isoformat(),
    }
