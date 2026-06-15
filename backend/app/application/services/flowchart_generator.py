from abc import ABC, abstractmethod

from app.application.dto.flowchart import FlowchartArtifact


class FlowchartGenerator(ABC):
    @abstractmethod
    def generate(self, activities: list[str], title: str | None = None) -> FlowchartArtifact:
        raise NotImplementedError
