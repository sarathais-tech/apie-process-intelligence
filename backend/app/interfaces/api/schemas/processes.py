from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.process import ProcessStatus


class ProcessStepRead(BaseModel):
    name: str
    order: int
    application: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class ProcessRead(BaseModel):
    id: UUID
    name: str
    status: ProcessStatus
    confidence_score: float
    created_at: datetime
    steps: list[ProcessStepRead]

    model_config = ConfigDict(from_attributes=True)
