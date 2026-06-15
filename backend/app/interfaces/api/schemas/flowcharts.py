from pydantic import BaseModel, Field


class FlowchartCreate(BaseModel):
    activities: list[str] = Field(min_length=1)
    title: str | None = None


class FlowchartRead(BaseModel):
    mermaid: str
    svg: str
    png_base64: str
    png_mime_type: str = "image/png"
    svg_mime_type: str = "image/svg+xml"
