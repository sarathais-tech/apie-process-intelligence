from abc import ABC, abstractmethod

from app.application.dto.sop import StandardOperatingProcedure, StandardOperatingProcedureArtifact


class StandardOperatingProcedureGenerator(ABC):
    @abstractmethod
    def generate(self, procedure: StandardOperatingProcedure) -> StandardOperatingProcedureArtifact:
        raise NotImplementedError
