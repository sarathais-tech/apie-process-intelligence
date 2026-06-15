from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.flowchart import FlowchartArtifact
from app.application.use_cases.generate_flowchart import GenerateFlowchartUseCase
from app.infrastructure.flowcharts.mermaid_flowchart_generator import MermaidFlowchartGenerator
from app.interfaces.api.dependencies import get_flowchart_generator
from app.interfaces.api.schemas.flowcharts import FlowchartCreate, FlowchartRead

router = APIRouter(prefix="/flowcharts", tags=["flowcharts"])

FlowchartGeneratorDep = Annotated[MermaidFlowchartGenerator, Depends(get_flowchart_generator)]


@router.post("", response_model=FlowchartRead, status_code=201)
def generate_flowchart(payload: FlowchartCreate, generator: FlowchartGeneratorDep) -> FlowchartArtifact:
    try:
        return GenerateFlowchartUseCase(generator).execute(payload.activities, title=payload.title)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
