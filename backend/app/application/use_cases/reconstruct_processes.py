from app.application.dto.process_discovery import ProcessDiscoveryResult, ProcessVariant
from app.application.services.process_discovery_engine import ProcessDiscoveryEngine
from app.domain.entities.process import ProcessStep, ReconstructedProcess
from app.domain.repositories.event_repository import EventRepository
from app.domain.repositories.process_repository import ProcessRepository


class ReconstructProcessesUseCase:
    def __init__(
        self,
        event_repository: EventRepository,
        process_repository: ProcessRepository,
        discovery_engine: ProcessDiscoveryEngine,
    ) -> None:
        self.event_repository = event_repository
        self.process_repository = process_repository
        self.discovery_engine = discovery_engine

    def execute(self, limit: int = 500) -> list[ReconstructedProcess]:
        events = self.event_repository.list(limit=limit, offset=0)
        discovery = self.discovery_engine.discover(events)
        processes: list[ReconstructedProcess] = []

        for index, variant in enumerate(discovery.variants, start=1):
            steps = self._build_steps(variant, discovery)
            if not steps:
                continue

            process = ReconstructedProcess(
                name=f"Fluxo descoberto {index} - {variant.frequency} execucao(oes)",
                steps=steps,
                confidence_score=self._confidence_score(variant, discovery),
            )
            processes.append(self.process_repository.add(process))

        return processes

    def _build_steps(self, variant: ProcessVariant, discovery: ProcessDiscoveryResult) -> list[ProcessStep]:
        steps: list[ProcessStep] = []

        for activity in variant.sequence:
            next_steps = self._next_steps(activity, discovery)
            steps.append(
                ProcessStep(
                    name=activity,
                    order=len(steps) + 1,
                    application=self._most_common_application(activity, variant),
                    metadata={
                        "frequency": variant.frequency,
                        "case_ids": list(variant.case_ids),
                        "next_steps": next_steps,
                        "pm4py_enabled": discovery.pm4py_enabled,
                    },
                )
            )

        return steps

    def _next_steps(self, activity: str, discovery: ProcessDiscoveryResult) -> list[dict[str, int | str]]:
        next_steps = [
            {"activity": target, "frequency": frequency}
            for (source, target), frequency in discovery.logical_flow.edges.items()
            if source == activity
        ]
        return sorted(next_steps, key=lambda item: (-int(item["frequency"]), str(item["activity"])))

    def _most_common_application(self, activity: str, variant: ProcessVariant) -> str | None:
        applications: dict[str, int] = {}
        for event in variant.events:
            event_activity = event.activity or event.window_title or event.process_name or event.event_type.value
            if event_activity != activity or not event.process_name:
                continue
            applications[event.process_name] = applications.get(event.process_name, 0) + 1

        if not applications:
            return None

        return sorted(applications.items(), key=lambda item: (-item[1], item[0]))[0][0]

    def _confidence_score(self, variant: ProcessVariant, discovery: ProcessDiscoveryResult) -> float:
        if discovery.total_cases == 0:
            return 0.0

        support = variant.frequency / discovery.total_cases
        sequence_weight = min(0.25, len(variant.sequence) * 0.03)
        pm4py_weight = 0.1 if discovery.pm4py_enabled else 0.0
        return round(min(0.98, 0.45 + support * 0.2 + sequence_weight + pm4py_weight), 2)
