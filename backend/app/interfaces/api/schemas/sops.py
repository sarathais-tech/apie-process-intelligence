from pydantic import BaseModel, Field


class SopFromFlowCreate(BaseModel):
    title: str = "Procedimento Operacional Padrao"
    activities: list[str] = Field(min_length=1)
    objective: str | None = None
    responsible_roles: list[str] | None = None
    prerequisites: list[str] | None = None
    expected_result: str | None = None


class SopFromProcessCreate(BaseModel):
    responsible_roles: list[str] | None = None
    prerequisites: list[str] | None = None


class SopRead(BaseModel):
    filename: str
    pdf_base64: str
    mime_type: str = "application/pdf"
