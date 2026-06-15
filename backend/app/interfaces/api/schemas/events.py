from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.event import EventType


class EventCreate(BaseModel):
    event_type: EventType
    source: str = Field(default="windows", max_length=100)
    user_id: str | None = None
    session_id: str | None = None
    process_name: str | None = None
    window_title: str | None = None
    activity: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EventRead(EventCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
