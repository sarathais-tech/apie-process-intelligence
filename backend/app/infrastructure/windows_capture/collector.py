from datetime import datetime, timezone
from getpass import getuser
from typing import Any
from uuid import uuid4

from app.domain.entities.event import EventType, UserEvent


class WindowsEventCollector:
    """Factory de eventos capturados no Windows.

    Os metodos sao pequenos de proposito: os listeners chamam esta classe e os
    testes validam a transformacao sem depender de hooks reais do sistema.
    """

    def __init__(self, session_id: str | None = None, user_id: str | None = None) -> None:
        self.session_id = session_id or str(uuid4())
        self.user_id = user_id or getuser()

    def build_mouse_click_event(
        self,
        x: int,
        y: int,
        button: str,
        pressed: bool,
        active_window: dict[str, str | None] | None = None,
    ) -> UserEvent:
        return self._build_event(
            event_type=EventType.MOUSE,
            activity="mouse_click",
            active_window=active_window,
            metadata={
                "action": "click",
                "x": x,
                "y": y,
                "button": button,
                "pressed": pressed,
            },
        )

    def build_mouse_move_event(
        self,
        x: int,
        y: int,
        active_window: dict[str, str | None] | None = None,
    ) -> UserEvent:
        return self._build_event(
            event_type=EventType.MOUSE,
            activity="mouse_move",
            active_window=active_window,
            metadata={"action": "move", "x": x, "y": y},
        )

    def build_key_press_event(
        self,
        key: str,
        active_window: dict[str, str | None] | None = None,
    ) -> UserEvent:
        return self._build_event(
            event_type=EventType.KEYBOARD,
            activity="key_press",
            active_window=active_window,
            metadata={"action": "key_press", "key": key},
        )

    def build_window_event(
        self,
        process_name: str | None,
        window_title: str | None,
        activity: str | None = None,
    ) -> UserEvent:
        return UserEvent(
            event_type=EventType.WINDOW,
            source="windows",
            user_id=self.user_id,
            session_id=self.session_id,
            process_name=process_name,
            window_title=window_title,
            activity=activity,
            occurred_at=datetime.now(timezone.utc),
            metadata={"collector": "WindowsEventCollector", "action": "active_window"},
        )

    def _build_event(
        self,
        event_type: EventType,
        activity: str,
        metadata: dict[str, Any],
        active_window: dict[str, str | None] | None,
    ) -> UserEvent:
        active_window = active_window or {}

        return UserEvent(
            event_type=event_type,
            source="windows",
            user_id=self.user_id,
            session_id=self.session_id,
            process_name=active_window.get("process_name"),
            window_title=active_window.get("window_title"),
            activity=activity,
            occurred_at=datetime.now(timezone.utc),
            metadata={"collector": "WindowsEventCollector", **metadata},
        )
