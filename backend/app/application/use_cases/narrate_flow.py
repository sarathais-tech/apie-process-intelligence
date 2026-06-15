from app.application.dto.narrative import FlowNarrative
from app.application.services.flow_narrator import FlowNarrator


class NarrateFlowUseCase:
    def __init__(self, narrator: FlowNarrator) -> None:
        self.narrator = narrator

    def execute(self, activities: list[str], model: str = "llama3") -> FlowNarrative:
        cleaned_activities = [activity.strip() for activity in activities if activity and activity.strip()]
        if not cleaned_activities:
            raise ValueError("O fluxo deve conter ao menos uma atividade.")

        return self.narrator.narrate(cleaned_activities, model=model)
