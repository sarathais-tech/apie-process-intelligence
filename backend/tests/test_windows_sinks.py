from app.domain.entities.event import EventType, UserEvent
from app.infrastructure.windows_capture.sinks import event_to_payload


def test_event_to_payload_serializes_event() -> None:
    event = UserEvent(
        event_type=EventType.MOUSE,
        source="windows",
        user_id="user-1",
        session_id="session-1",
        process_name="app.exe",
        window_title="Tela",
        activity="mouse_click",
        metadata={"x": 1, "y": 2},
    )

    payload = event_to_payload(event)

    assert payload["event_type"] == "mouse"
    assert payload["source"] == "windows"
    assert payload["user_id"] == "user-1"
    assert payload["session_id"] == "session-1"
    assert payload["process_name"] == "app.exe"
    assert payload["window_title"] == "Tela"
    assert payload["activity"] == "mouse_click"
    assert payload["metadata"] == {"x": 1, "y": 2}
    assert isinstance(payload["occurred_at"], str)
