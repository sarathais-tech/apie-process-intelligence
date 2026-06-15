from app.application.dto.flowchart import FlowchartArtifact
from app.application.services.flowchart_generator import FlowchartGenerator


class GenerateFlowchartUseCase:
    def __init__(self, generator: FlowchartGenerator) -> None:
        self.generator = generator

    def execute(self, activities: list[str], title: str | None = None) -> FlowchartArtifact:
        cleaned_activities = [activity.strip() for activity in activities if activity and activity.strip()]
        if not cleaned_activities:
            raise ValueError("A sequencia deve conter ao menos uma atividade.")

        return self.generator.generate(cleaned_activities, title=title)
