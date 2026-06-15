from app.domain.entities.event import EventType
from app.infrastructure.windows_capture.collector import WindowsEventCollector


def test_build_mouse_click_event() -> None:
    collector = WindowsEventCollector(session_id="session-1", user_id="user-1")

    event = collector.build_mouse_click_event(
        x=10,
        y=20,
        button="Button.left",
        pressed=True,
        active_window={"process_name": "chrome.exe", "window_title": "ERP"},
    )

    assert event.event_type == EventType.MOUSE
    assert event.activity == "mouse_click"
    assert event.user_id == "user-1"
    assert event.session_id == "session-1"
    assert event.process_name == "chrome.exe"
    assert event.window_title == "ERP"
    assert event.metadata["action"] == "click"
    assert event.metadata["x"] == 10
    assert event.metadata["y"] == 20
    assert event.metadata["button"] == "Button.left"
    assert event.metadata["pressed"] is True


def test_build_mouse_move_event() -> None:
    collector = WindowsEventCollector(session_id="session-1", user_id="user-1")

    event = collector.build_mouse_move_event(
        x=30,
        y=40,
        active_window={"process_name": "excel.exe", "window_title": "Planilha"},
    )

    assert event.event_type == EventType.MOUSE
    assert event.activity == "mouse_move"
    assert event.metadata["action"] == "move"
    assert event.metadata["x"] == 30
    assert event.metadata["y"] == 40


def test_build_key_press_event() -> None:
    collector = WindowsEventCollector(session_id="session-1", user_id="user-1")

    event = collector.build_key_press_event(
        key="a",
        active_window={"process_name": "notepad.exe", "window_title": "Notas"},
    )

    assert event.event_type == EventType.KEYBOARD
    assert event.activity == "key_press"
    assert event.metadata["action"] == "key_press"
    assert event.metadata["key"] == "a"


def test_build_window_event() -> None:
    collector = WindowsEventCollector(session_id="session-1", user_id="user-1")

    event = collector.build_window_event(
        process_name="code.exe",
        window_title="APIE",
        activity="active_window_changed",
    )

    assert event.event_type == EventType.WINDOW
    assert event.activity == "active_window_changed"
    assert event.process_name == "code.exe"
    assert event.window_title == "APIE"
    assert event.metadata["action"] == "active_window"
