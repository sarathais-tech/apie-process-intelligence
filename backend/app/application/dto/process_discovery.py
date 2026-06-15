from dataclasses import dataclass, field

from app.domain.entities.event import UserEvent


@dataclass(frozen=True)
class ProcessVariant:
    sequence: tuple[str, ...]
    frequency: int
    case_ids: tuple[str, ...]
    events: tuple[UserEvent, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class LogicalFlow:
    edges: dict[tuple[str, str], int]
    start_activities: dict[str, int]
    end_activities: dict[str, int]


@dataclass(frozen=True)
class ProcessDiscoveryResult:
    variants: list[ProcessVariant]
    logical_flow: LogicalFlow
    total_cases: int
    total_events: int
    pm4py_enabled: bool
