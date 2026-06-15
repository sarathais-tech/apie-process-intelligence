import threading
import time

from app.domain.entities.event import UserEvent
from app.infrastructure.windows_capture.active_window import ActiveWindowReader
from app.infrastructure.windows_capture.collector import WindowsEventCollector
from app.infrastructure.windows_capture.sinks import EventSink


class WindowsEventMonitor:
    def __init__(
        self,
        sink: EventSink,
        collector: WindowsEventCollector | None = None,
        active_window_reader: ActiveWindowReader | None = None,
        mouse_move_interval_seconds: float = 0.25,
        window_poll_interval_seconds: float = 1.0,
    ) -> None:
        self.sink = sink
        self.collector = collector or WindowsEventCollector()
        self.active_window_reader = active_window_reader or ActiveWindowReader()
        self.mouse_move_interval_seconds = mouse_move_interval_seconds
        self.window_poll_interval_seconds = window_poll_interval_seconds
        self._last_mouse_move_at = 0.0
        self._last_window_signature: tuple[str | None, str | None] | None = None
        self._stop_event = threading.Event()

    def on_click(self, x: int, y: int, button: object, pressed: bool) -> UserEvent:
        event = self.collector.build_mouse_click_event(
            x=x,
            y=y,
            button=str(button),
            pressed=pressed,
            active_window=self.active_window_reader.read().as_dict(),
        )
        return self.sink.save(event)

    def on_move(self, x: int, y: int) -> UserEvent | None:
        now = time.monotonic()
        if now - self._last_mouse_move_at < self.mouse_move_interval_seconds:
            return None

        self._last_mouse_move_at = now
        event = self.collector.build_mouse_move_event(
            x=x,
            y=y,
            active_window=self.active_window_reader.read().as_dict(),
        )
        return self.sink.save(event)

    def on_press(self, key: object) -> UserEvent:
        event = self.collector.build_key_press_event(
            key=self._format_key(key),
            active_window=self.active_window_reader.read().as_dict(),
        )
        return self.sink.save(event)

    def poll_active_window_once(self) -> UserEvent | None:
        active_window = self.active_window_reader.read()
        signature = (active_window.process_name, active_window.window_title)
        if signature == self._last_window_signature:
            return None

        self._last_window_signature = signature
        event = self.collector.build_window_event(
            process_name=active_window.process_name,
            window_title=active_window.window_title,
            activity="active_window_changed",
        )
        return self.sink.save(event)

    def start(self) -> None:
        try:
            from pynput import keyboard, mouse
        except ImportError as exc:
            raise RuntimeError("Instale pynput para capturar mouse e teclado no Windows.") from exc

        self._stop_event.clear()
        window_thread = threading.Thread(target=self._poll_active_window_loop, daemon=True)
        window_thread.start()

        mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_press)

        mouse_listener.start()
        keyboard_listener.start()

        try:
            while not self._stop_event.is_set():
                time.sleep(0.2)
        finally:
            mouse_listener.stop()
            keyboard_listener.stop()
            window_thread.join(timeout=2)

    def stop(self) -> None:
        self._stop_event.set()

    def _poll_active_window_loop(self) -> None:
        while not self._stop_event.is_set():
            self.poll_active_window_once()
            time.sleep(self.window_poll_interval_seconds)

    def _format_key(self, key: object) -> str:
        char = getattr(key, "char", None)
        if char:
            return char
        return str(key)
