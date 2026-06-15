from dataclasses import dataclass


@dataclass(frozen=True)
class FlowchartArtifact:
    mermaid: str
    svg: str
    png_base64: str
    png_mime_type: str = "image/png"
    svg_mime_type: str = "image/svg+xml"
