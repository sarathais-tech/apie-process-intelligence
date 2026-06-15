from dataclasses import dataclass

from app.infrastructure.windows_capture.active_window import ActiveWindow
from app.infrastructure.windows_capture.collector import WindowsEventCollector
from app.infrastructure.windows_capture.monitor import WindowsEventMonitor
from app.infrastructure.windows_capture.sinks import InMemoryEventSink


class FakeWindowReader:
    def __init__(self) -> None:
        self.window = ActiveWindow(process_name="app.exe", window_title="Tela inicial")

    def read(self) -> ActiveWindow:
        return self.window


@dataclass
class FakeKey:
    char: str | None = None

    def __str__(self) -> str:
        return "Key.enter"


def build_monitor() -> tuple[WindowsEventMonitor, InMemoryEventSink, FakeWindowReader]:
    sink = InMemoryEventSink()
    reader = FakeWindowReader()
    monitor = WindowsEventMonitor(
        sink=sink,
        collector=WindowsEventCollector(session_id="session-1", user_id="user-1"),
        active_window_reader=reader,
        mouse_move_interval_seconds=0,
    )
    return monitor, sink, reader


def test_on_click_saves_mouse_click_event() -> None:
    monitor, sink, _ = build_monitor()

    event = monitor.on_click(100, 200, "Button.left", True)

    assert sink.events == [event]
    assert event.activity == "mouse_click"
    assert event.metadata["x"] == 100
    assert event.metadata["y"] == 200
    assert event.process_name == "app.exe"


def test_on_move_saves_mouse_move_event() -> None:
    monitor, sink, _ = build_monitor()

    event = monitor.on_move(50, 60)

    assert sink.events == [event]
    assert event is not None
    assert event.activity == "mouse_move"
    assert event.metadata["x"] == 50
    assert event.metadata["y"] == 60


def test_on_press_saves_key_press_event() -> None:
    monitor, sink, _ = build_monitor()

    event = monitor.on_press(FakeKey(char="x"))

    assert sink.events == [event]
    assert event.activity == "key_press"
    assert event.metadata["key"] == "x"


def test_on_press_formats_special_key() -> None:
    monitor, sink, _ = build_monitor()

    event = monitor.on_press(FakeKey())

    assert sink.events == [event]
    assert event.metadata["key"] == "Key.enter"


def test_poll_active_window_saves_only_when_window_changes() -> None:
    monitor, sink, reader = build_monitor()

    first = monitor.poll_active_window_once()
    second = monitor.poll_active_window_once()
    reader.window = ActiveWindow(process_name="code.exe", window_title="APIE")
    third = monitor.poll_active_window_once()

    assert first is not None
    assert second is None
    assert third is not None
    assert len(sink.events) == 2
    assert sink.events[0].process_name == "app.exe"
    assert sink.events[1].process_name == "code.exe"
