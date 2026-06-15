from abc import ABC, abstractmethod

from app.application.dto.process_discovery import ProcessDiscoveryResult
from app.domain.entities.event import UserEvent


class ProcessDiscoveryEngine(ABC):
    @abstractmethod
    def discover(self, events: list[UserEvent]) -> ProcessDiscoveryResult:
        raise NotImplementedError
