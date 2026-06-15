from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

from app.application.dto.process_discovery import LogicalFlow, ProcessDiscoveryResult, ProcessVariant
from app.application.services.process_discovery_engine import ProcessDiscoveryEngine
from app.domain.entities.event import UserEvent


@dataclass(frozen=True)
class CaseTrace:
    case_id: str
    events: tuple[UserEvent, ...]
    sequence: tuple[str, ...]


class PM4PyProcessDiscoveryEngine(ProcessDiscoveryEngine):
    def discover(self, events: list[UserEvent]) -> ProcessDiscoveryResult:
        traces = self._build_case_traces(events)
        pm4py_enabled = self._touch_pm4py_event_log(traces)
        variants = self._discover_repeated_variants(traces)
        flow = self._build_logical_flow(traces)

        return ProcessDiscoveryResult(
            variants=variants,
            logical_flow=flow,
            total_cases=len(traces),
            total_events=sum(len(trace.events) for trace in traces),
            pm4py_enabled=pm4py_enabled,
        )

    def _build_case_traces(self, events: list[UserEvent]) -> list[CaseTrace]:
        grouped: dict[str, list[UserEvent]] = defaultdict(list)
        for event in events:
            grouped[event.session_id or "default"].append(event)

        traces: list[CaseTrace] = []
        for case_id, case_events in grouped.items():
            ordered_events = tuple(sorted(case_events, key=lambda event: event.occurred_at))
            sequence = tuple(self._activity_name(event) for event in ordered_events)
            compact_sequence = self._compact_repeated_neighbors(sequence)
            traces.append(CaseTrace(case_id=case_id, events=ordered_events, sequence=compact_sequence))

        return sorted(traces, key=lambda trace: trace.case_id)

    def _discover_repeated_variants(self, traces: list[CaseTrace]) -> list[ProcessVariant]:
        cases_by_sequence: dict[tuple[str, ...], list[str]] = defaultdict(list)
        events_by_sequence: dict[tuple[str, ...], list[UserEvent]] = defaultdict(list)

        for trace in traces:
            if not trace.sequence:
                continue
            cases_by_sequence[trace.sequence].append(trace.case_id)
            events_by_sequence[trace.sequence].extend(trace.events)

        variants = [
            ProcessVariant(
                sequence=sequence,
                frequency=len(case_ids),
                case_ids=tuple(case_ids),
                events=tuple(events_by_sequence[sequence]),
            )
            for sequence, case_ids in cases_by_sequence.items()
        ]

        return sorted(variants, key=lambda variant: (-variant.frequency, variant.sequence))

    def _build_logical_flow(self, traces: list[CaseTrace]) -> LogicalFlow:
        edges: Counter[tuple[str, str]] = Counter()
        start_activities: Counter[str] = Counter()
        end_activities: Counter[str] = Counter()

        for trace in traces:
            if not trace.sequence:
                continue
            start_activities[trace.sequence[0]] += 1
            end_activities[trace.sequence[-1]] += 1
            edges.update(zip(trace.sequence, trace.sequence[1:]))

        return LogicalFlow(
            edges=dict(edges),
            start_activities=dict(start_activities),
            end_activities=dict(end_activities),
        )

    def _touch_pm4py_event_log(self, traces: list[CaseTrace]) -> bool:
        try:
            import pandas as pd
            import pm4py
        except ImportError:
            return False

        rows: list[dict[str, Any]] = []
        for trace in traces:
            for event in trace.events:
                rows.append(
                    {
                        "case:concept:name": trace.case_id,
                        "concept:name": self._activity_name(event),
                        "time:timestamp": event.occurred_at,
                    }
                )

        if not rows:
            return True

        dataframe = pd.DataFrame(rows)
        pm4py.format_dataframe(
            dataframe,
            case_id="case:concept:name",
            activity_key="concept:name",
            timestamp_key="time:timestamp",
        )
        return True

    def _activity_name(self, event: UserEvent) -> str:
        if event.activity:
            return event.activity
        if event.window_title:
            return event.window_title
        if event.process_name:
            return event.process_name
        return event.event_type.value

    def _compact_repeated_neighbors(self, sequence: tuple[str, ...]) -> tuple[str, ...]:
        compacted: list[str] = []
        for activity in sequence:
            if compacted and compacted[-1] == activity:
                continue
            compacted.append(activity)
        return tuple(compacted)
