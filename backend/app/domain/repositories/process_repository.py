from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.process import ReconstructedProcess


class ProcessRepository(ABC):
    @abstractmethod
    def add(self, process: ReconstructedProcess) -> ReconstructedProcess:
        raise NotImplementedError

    @abstractmethod
    def list(self, limit: int = 100, offset: int = 0) -> list[ReconstructedProcess]:
        raise NotImplementedError

    @abstractmethod
    def get(self, process_id: UUID) -> ReconstructedProcess | None:
        raise NotImplementedError
