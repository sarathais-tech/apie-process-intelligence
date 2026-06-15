from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.event import EventType, UserEvent
from app.domain.repositories.event_repository import EventRepository
from app.infrastructure.database.models import EventModel


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, event: UserEvent) -> UserEvent:
        model = EventModel(
            id=event.id,
            event_type=event.event_type.value,
            source=event.source,
            user_id=event.user_id,
            session_id=event.session_id,
            process_name=event.process_name,
            window_title=event.window_title,
            activity=event.activity,
            event_metadata=event.metadata,
            occurred_at=event.occurred_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def list(self, limit: int = 100, offset: int = 0) -> list[UserEvent]:
        statement = select(EventModel).order_by(EventModel.occurred_at.desc()).limit(limit).offset(offset)
        return [self._to_entity(model) for model in self.db.scalars(statement).all()]

    def get(self, event_id: UUID) -> UserEvent | None:
        model = self.db.get(EventModel, event_id)
        return self._to_entity(model) if model else None

    def _to_entity(self, model: EventModel) -> UserEvent:
        return UserEvent(
            id=model.id,
            event_type=EventType(model.event_type),
            source=model.source,
            user_id=model.user_id,
            session_id=model.session_id,
            process_name=model.process_name,
            window_title=model.window_title,
            activity=model.activity,
            metadata=model.event_metadata,
            occurred_at=model.occurred_at,
        )
