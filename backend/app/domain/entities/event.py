from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class EventType(StrEnum):
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    WINDOW = "window"
    APPLICATION = "application"
    SYSTEM = "system"


@dataclass(frozen=True)
class UserEvent:
    event_type: EventType
    source: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: UUID = field(default_factory=uuid4)
    user_id: str | None = None
    session_id: str | None = None
    process_name: str | None = None
    window_title: str | None = None
    activity: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
