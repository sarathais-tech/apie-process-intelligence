from dataclasses import dataclass


@dataclass(frozen=True)
class ActiveWindow:
    process_name: str | None
    window_title: str | None

    def as_dict(self) -> dict[str, str | None]:
        return {"process_name": self.process_name, "window_title": self.window_title}


class ActiveWindowReader:
    def read(self) -> ActiveWindow:
        try:
            import win32gui
            import win32process
            import psutil
        except ImportError:
            return ActiveWindow(process_name=None, window_title=None)

        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return ActiveWindow(process_name=None, window_title=None)

        window_title = win32gui.GetWindowText(hwnd) or None
        _, process_id = win32process.GetWindowThreadProcessId(hwnd)

        try:
            process_name = psutil.Process(process_id).name()
        except Exception:
            process_name = None

        return ActiveWindow(process_name=process_name, window_title=window_title)
