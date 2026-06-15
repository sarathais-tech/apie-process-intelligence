from pydantic import BaseModel, Field


class FlowNarrativeCreate(BaseModel):
    activities: list[str] = Field(min_length=1)
    model: str = "llama3"


class FlowNarrativeRead(BaseModel):
    text: str
    model: str
    provider: str
    used_fallback: bool = False
