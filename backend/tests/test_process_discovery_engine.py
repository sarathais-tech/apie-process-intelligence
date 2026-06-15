from datetime import datetime, timedelta, timezone

from app.domain.entities.event import EventType, UserEvent
from app.infrastructure.process_mining.pm4py_discovery_engine import PM4PyProcessDiscoveryEngine


def make_event(session_id: str, activity: str, seconds: int, process_name: str = "app.exe") -> UserEvent:
    return UserEvent(
        event_type=EventType.WINDOW,
        source="windows",
        session_id=session_id,
        process_name=process_name,
        activity=activity,
        occurred_at=datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=seconds),
    )


def test_discover_identifies_repeated_sequences() -> None:
    events = [
        make_event("case-1", "abrir_pedido", 1),
        make_event("case-1", "validar_pedido", 2),
        make_event("case-1", "finalizar_pedido", 3),
        make_event("case-2", "abrir_pedido", 4),
        make_event("case-2", "validar_pedido", 5),
        make_event("case-2", "finalizar_pedido", 6),
        make_event("case-3", "abrir_pedido", 7),
        make_event("case-3", "cancelar_pedido", 8),
    ]

    result = PM4PyProcessDiscoveryEngine().discover(events)

    assert result.total_cases == 3
    assert result.total_events == 8
    assert result.variants[0].sequence == ("abrir_pedido", "validar_pedido", "finalizar_pedido")
    assert result.variants[0].frequency == 2
    assert result.variants[0].case_ids == ("case-1", "case-2")


def test_discover_groups_similar_executions_and_generates_logical_flow() -> None:
    events = [
        make_event("case-1", "login", 1),
        make_event("case-1", "buscar_cliente", 2),
        make_event("case-1", "salvar", 3),
        make_event("case-2", "login", 4),
        make_event("case-2", "buscar_cliente", 5),
        make_event("case-2", "salvar", 6),
        make_event("case-3", "login", 7),
        make_event("case-3", "buscar_cliente", 8),
        make_event("case-3", "revisar", 9),
        make_event("case-3", "salvar", 10),
    ]

    result = PM4PyProcessDiscoveryEngine().discover(events)

    assert len(result.variants) == 2
    assert result.logical_flow.start_activities == {"login": 3}
    assert result.logical_flow.end_activities == {"salvar": 3}
    assert result.logical_flow.edges[("login", "buscar_cliente")] == 3
    assert result.logical_flow.edges[("buscar_cliente", "salvar")] == 2
    assert result.logical_flow.edges[("buscar_cliente", "revisar")] == 1
    assert result.logical_flow.edges[("revisar", "salvar")] == 1


def test_discover_compacts_neighbor_repetitions() -> None:
    events = [
        make_event("case-1", "digitar", 1),
        make_event("case-1", "digitar", 2),
        make_event("case-1", "salvar", 3),
    ]

    result = PM4PyProcessDiscoveryEngine().discover(events)

    assert result.variants[0].sequence == ("digitar", "salvar")
