import argparse

from app.infrastructure.windows_capture.monitor import WindowsEventMonitor
from app.infrastructure.windows_capture.sinks import ApiEventSink, PostgresEventSink


def run_agent(api_url: str = "http://localhost:8000/api/v1/events", sink_type: str = "api") -> None:
    sink = PostgresEventSink() if sink_type == "postgres" else ApiEventSink(api_url=api_url)
    WindowsEventMonitor(sink=sink).start()


def main() -> None:
    parser = argparse.ArgumentParser(description="APIE Windows event capture agent")
    parser.add_argument("--api-url", default="http://localhost:8000/api/v1/events")
    parser.add_argument("--sink", choices=["api", "postgres"], default="api")
    args = parser.parse_args()
    run_agent(api_url=args.api_url, sink_type=args.sink)


if __name__ == "__main__":
    main()
