from dataclasses import dataclass


@dataclass(frozen=True)
class FlowNarrative:
    text: str
    model: str
    provider: str
    used_fallback: bool = False
