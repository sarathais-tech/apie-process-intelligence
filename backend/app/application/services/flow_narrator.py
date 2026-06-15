from abc import ABC, abstractmethod

from app.application.dto.narrative import FlowNarrative


class FlowNarrator(ABC):
    @abstractmethod
    def narrate(self, activities: list[str], model: str = "llama3") -> FlowNarrative:
        raise NotImplementedError
