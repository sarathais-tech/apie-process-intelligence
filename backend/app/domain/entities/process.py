from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class ProcessStatus(StrEnum):
    DISCOVERED = "discovered"
    REVIEWED = "reviewed"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class ProcessStep:
    name: str
    order: int
    application: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReconstructedProcess:
    name: str
    steps: list[ProcessStep]
    id: UUID = field(default_factory=uuid4)
    status: ProcessStatus = ProcessStatus.DISCOVERED
    confidence_score: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
