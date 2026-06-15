from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.application.use_cases.list_events import ListEventsUseCase
from app.application.use_cases.record_event import RecordEventUseCase
from app.domain.entities.event import UserEvent
from app.infrastructure.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.interfaces.api.dependencies import get_event_repository
from app.interfaces.api.schemas.events import EventCreate, EventRead

router = APIRouter(prefix="/events", tags=["events"])


EventRepo = Annotated[SqlAlchemyEventRepository, Depends(get_event_repository)]


@router.post("", response_model=EventRead, status_code=201)
def create_event(payload: EventCreate, repository: EventRepo) -> UserEvent:
    event = UserEvent(**payload.model_dump())
    return RecordEventUseCase(repository).execute(event)


@router.get("", response_model=list[EventRead])
def list_events(
    repository: EventRepo,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[UserEvent]:
    return ListEventsUseCase(repository).execute(limit=limit, offset=offset)


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: UUID, repository: EventRepo) -> UserEvent:
    event = repository.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento nao encontrado")
    return event
