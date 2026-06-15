from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.application.use_cases.reconstruct_processes import ReconstructProcessesUseCase
from app.domain.entities.event import EventType, UserEvent
from app.domain.entities.process import ReconstructedProcess
from app.domain.repositories.event_repository import EventRepository
from app.domain.repositories.process_repository import ProcessRepository
from app.infrastructure.process_mining.pm4py_discovery_engine import PM4PyProcessDiscoveryEngine


class FakeEventRepository(EventRepository):
    def __init__(self, events: list[UserEvent]) -> None:
        self.events = events

    def add(self, event: UserEvent) -> UserEvent:
        self.events.append(event)
        return event

    def list(self, limit: int = 100, offset: int = 0) -> list[UserEvent]:
        return self.events[offset : offset + limit]

    def get(self, event_id: UUID) -> UserEvent | None:
        return next((event for event in self.events if event.id == event_id), None)


class FakeProcessRepository(ProcessRepository):
    def __init__(self) -> None:
        self.processes: list[ReconstructedProcess] = []

    def add(self, process: ReconstructedProcess) -> ReconstructedProcess:
        self.processes.append(process)
        return process

    def list(self, limit: int = 100, offset: int = 0) -> list[ReconstructedProcess]:
        return self.processes[offset : offset + limit]

    def get(self, process_id: UUID) -> ReconstructedProcess | None:
        return next((process for process in self.processes if process.id == process_id), None)


def make_event(session_id: str, activity: str, seconds: int, process_name: str = "erp.exe") -> UserEvent:
    return UserEvent(
        event_type=EventType.WINDOW,
        source="windows",
        session_id=session_id,
        process_name=process_name,
        activity=activity,
        occurred_at=datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=seconds),
    )


def test_reconstruct_processes_generates_processes_from_discovered_variants() -> None:
    events = [
        make_event("case-1", "login", 1),
        make_event("case-1", "consultar", 2),
        make_event("case-1", "salvar", 3),
        make_event("case-2", "login", 4),
        make_event("case-2", "consultar", 5),
        make_event("case-2", "salvar", 6),
    ]
    process_repository = FakeProcessRepository()
    use_case = ReconstructProcessesUseCase(
        event_repository=FakeEventRepository(events),
        process_repository=process_repository,
        discovery_engine=PM4PyProcessDiscoveryEngine(),
    )

    processes = use_case.execute()

    assert len(processes) == 1
    assert process_repository.processes == processes
    assert processes[0].name == "Fluxo descoberto 1 - 2 execucao(oes)"
    assert [step.name for step in processes[0].steps] == ["login", "consultar", "salvar"]
    assert processes[0].steps[0].metadata["frequency"] == 2
    assert processes[0].steps[0].metadata["next_steps"] == [{"activity": "consultar", "frequency": 2}]
