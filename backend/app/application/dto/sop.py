from dataclasses import dataclass

from app.domain.entities.process import ProcessStep


@dataclass(frozen=True)
class StandardOperatingProcedure:
    title: str
    objective: str
    responsible_roles: list[str]
    prerequisites: list[str]
    steps: list[ProcessStep]
    expected_result: str


@dataclass(frozen=True)
class StandardOperatingProcedureArtifact:
    filename: str
    pdf_base64: str
    mime_type: str = "application/pdf"
